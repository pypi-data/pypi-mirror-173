#!/usr/bin/python
import argparse
import MySQLdb
import MySQLdb.cursors
from getpass import getpass
from dataclasses import dataclass, field
import curses
from threading import Thread
import sys
import plotille
import numpy as np
from cusser import Cusser

from datetime import datetime
from time import perf_counter, sleep

@dataclass
class QueryOptions:
    db_host: str
    db_user: str | None
    db_pass: str | None
    db_base: str | None
    db_port: int | None
    query: str
    graph_values: str
    graph_labels: str
    graph_max_samples: int
    vertical: bool

    last_run: datetime = datetime.now()
    running: bool = False
    execution_time: float = 0

    _result: list = field(default_factory=list)
    graph_x: int = 0
    graph_data: dict = field(default_factory=dict)
    graph_max_width: int = 10
    graph_max_height: int = 10

    columns: list = field(default_factory=list)
    width: list = field(default_factory=list)

    @property
    def result(self) -> list: return self._result

    @result.setter
    def result(self, value):
        self._result = value
        self.columns = list({val for row in self._result for val in row.keys()})
        self.width = [len(x) for x in self.columns]
        for i, row in enumerate(self.result):
            for key, value in row.items():
                col_i = self.columns.index(key)
                if value is not None:
                    self.width[col_i] = max(self.width[col_i], len(str(value)))
        for row in self.result:
            label = None
            value = None
            for _label, _value in row.items():
                if _label == self.graph_labels:
                    label = _value
                if _label == self.graph_values:
                    value = _value
            if label not in self.graph_data: self.graph_data[label] = []
            if len(self.graph_data[label]) > self.graph_max_samples:
                self.graph_data[label] = self.graph_data[label][-self.graph_max_samples-1:]
            self.graph_data[label].append((self.graph_x, value))
        self.graph_x += 1

    @property
    def result_count(self) -> int: return len(self.result)

class DBConnection:
    """ Context manager, that CAN be used "manually" with the open and close methods. """

    def __init__(self, queryOptions: QueryOptions, cursorclass=MySQLdb.cursors.DictCursor, **params):
        self.cursorclass = cursorclass
        self.connect_params = {
            "host": queryOptions.db_host,
            "user": queryOptions.db_user,
            "passwd": queryOptions.db_pass,
            "db": queryOptions.db_base,
            "port": queryOptions.db_port,
            "charset": "latin1",
            "use_unicode": True
        }
        for key, value in params.items(): self.connect_params[key] = value
        if open: self.open()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        """ This should run even if a exception is raised somewhere. """
        self.close()

    def open(self):
        self.cnx = MySQLdb.connect(**self.connect_params)
        self.cur = self.cnx.cursor(self.cursorclass)

    def close(self):
        if hasattr(self, "cur") and hasattr(self, "cnx") and self.cnx.open:
            self.cur.close()
            self.cnx.close()

def table_vertical(data):
    margin = max(max([len(y) for y in x.keys()]) for x in data)
    out = ""
    for i, row in enumerate(data):
        out += f"*************************** {i}. row ***************************\n"
        for key, value in row.items():
            out += f"{key:>{margin}}: {value}\n"
    return out

class WatchSQL:

    def __init__(self, query: QueryOptions, timeout: int, vertical_table: bool):
        self.db = DBConnection(query)
        self.query = query
        self.timeout = timeout
        self.vertical_table = vertical_table

        self.pause = False
        self.last_command_run_s = float("-inf")

        self.graph_data = []

        self.lines, self.columns = 0, 0
        self.cur_x, self.cur_y = 0, 0
        self.table_min, self.table_max = 0, 0

        self.screen_change_pending = False
        self.query_had_error = False
        self.query_error = None

    def __del__(self):
        if self.db is not None: self.db.close()

    def open_watch_curses(self):
        self.db.open()
        curses.wrapper(self._watch_curses)

    def _watch_curses(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.erase()
        stdscr.refresh()

        self.screen_change_pending = True
        self.table_win = stdscr.derwin(1,0)
        self.table_win_lines = 10
        self.table_win_show = self.query.graph_values is None
        self.graph_win = stdscr.derwin(1,0)
        self.graph_win_lines = 10
        self.graph_win_show = self.query.graph_values is not None
        self.graph_win_cansi = Cusser(self.graph_win)
        self.graph_win_cansi.color_manager.next_color_index = 50
        self.graph_win_cansi.color_manager.next_pair_index = 50

        #curses.start_color()
        curses.init_color(200, 255, 0, 0)
        curses.init_pair(1, curses.COLOR_CYAN,  curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, 200)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(6, 200, -1)

        k = 0
        while k != ord('q'):
            if (not self.pause) and (not self.query.running) and (perf_counter() - self.last_command_run_s > self.timeout):
                Thread(target=self._watch).start()

            lines, columns = stdscr.getmaxyx()
            if (lines != self.lines) or (columns != self.columns):
                self.lines, self.columns, self.screen_change_pending = lines, columns, True

            if self.screen_change_pending:
                self.query.graph_max_width, self.query.graph_max_height = self.columns, self.lines

                stdscr.erase()
                self._curses_topbar(stdscr)
                self._curses_graph_win(self.graph_win)
                self._curses_table_win(self.table_win)
                self._curses_bottombar(stdscr)
                stdscr.refresh()

                self.screen_change_pending = False

            self._curses_key_handle(k, stdscr)
            k = stdscr.getch()
            sleep(0.01)

    def _curses_key_handle(self, k, stdscr):
        if k in [ord('0'), ord('^')]:
            self.cur_y = 0
            self.cur_x = 0
            self.screen_change_pending = True
        elif k in [curses.KEY_DOWN, ord('j')]:
            self.cur_y = self.cur_y + 1
            self.screen_change_pending = True
        elif k in [curses.KEY_UP, ord('k')]:
            self.cur_y = max(0, self.cur_y - 1)
            self.screen_change_pending = True
        elif k in [curses.KEY_RIGHT, ord('l')]:
            self.cur_x = self.cur_x + 1
            self.screen_change_pending = True
        elif k in [curses.KEY_LEFT, ord('h')]:
            self.cur_x = max(0, self.cur_x - 1)
            self.screen_change_pending = True
        elif k in [curses.KEY_NPAGE]:
            self.cur_y = self.cur_y + self.lines
            self.screen_change_pending = True
        elif k in [curses.KEY_PPAGE]:
            self.cur_y = max(0, self.cur_y - self.lines)
            self.screen_change_pending = True
        elif k in [ord("G")]:
            self.cur_y = len(self.query.result) - 1
            self.screen_change_pending = True
        elif k in [27]:
            if (kk := stdscr.getch()) != -1:
                self.query_had_error = True
                self.query_error = kk
                self.screen_change_pending = True
        elif k in [curses.KEY_F3]:
            if (self.query.graph_values is None) or (not self.graph_win_show):
                self.query_had_error = True
                self.query_error = "Cannot hide only open window"
            else:
                self.table_win_show = not self.table_win_show
            self.screen_change_pending = True
        elif k in [curses.KEY_F4]:
            if self.query.graph_values is None:
                self.query_had_error = True
                self.query_error = "No graph column selected"
            if not self.table_win_show:
                self.query_had_error = True
                self.query_error = "Cannot hide only open window"
            else:
                self.graph_win_show = not self.graph_win_show
            self.screen_change_pending = True
        elif k in [curses.KEY_F5]:
            self.pause = not self.pause
            self.screen_change_pending = True

    def _curses_topbar(self, stdscr):
        colorpair = curses.color_pair(3)
        statusstr = f" {self.query.last_run.strftime('%Y-%m-%d %H:%M:%S')} ┃"
        if self.pause:
            colorpair = curses.color_pair(5)
            statusstr += " PAUSED ┃ "
        else:
            statusstr += f" Every {self.timeout} s ┃ "
        statusstr += "Query running..." if self.query.running else f"{self.query.result_count} rows in {self.query.execution_time:2.2f} s"
        pos = f"┃[{self.cur_y}:{self.cur_x}]"
        statusstr += " " * (self.columns-len(statusstr)-len(pos))
        statusstr += pos
        stdscr.attron(colorpair)
        stdscr.addstr(0, 0, statusstr[0:self.columns])
        stdscr.attroff(colorpair)

    def _curses_bottombar(self, stdscr):
        colorpair = curses.color_pair(3)
        if self.query_had_error:
            colorpair = curses.color_pair(4)
            statusstr = f"Query error: {self.query_error}"
        else:
            statusstr = " q: Quit"
            if self.query.graph_values is not None:
                statusstr += f" ┃ F3: {'Hide' if self.table_win_show else 'Show'} Table"
                statusstr += f" ┃ F4: {'Hide' if self.graph_win_show else 'Show'} graph"
            statusstr += f" ┃ F5: {'Resume' if self.pause else 'Pause'}"
        stdscr.attron(colorpair)
        stdscr.addstr(self.lines-2, 0, f"{statusstr:{self.columns}}")
        stdscr.attroff(colorpair)

    def _curses_table_win(self, twin):
        hlines = 1
        if self.table_win_show and self.graph_win_show:
            self.table_win_lines = self.lines // 2
            if len(self.query.result) < self.table_win_lines:
                self.table_win_lines = len(self.query.result) + hlines + 1
        elif self.table_win_show:
            hlines += 1
            self.table_win_lines = self.lines - 1 - hlines
        else: return

        twin.resize(1,1)
        twin.mvderwin(max(self.lines-self.table_win_lines-hlines, 0), 0)
        twin.resize(self.table_win_lines, self.columns)

        if self.cur_y < self.table_min:
            self.table_min = self.cur_y
        if self.table_max - self.table_min != self.table_win_lines - hlines:
            self.table_max = self.table_min + self.table_win_lines - hlines
        self.cur_y = min(self.cur_y, max(0, self.query.result_count - 1))
        if self.cur_y >= self.table_max:
            self.table_max = self.cur_y
            self.table_min = self.cur_y - self.table_win_lines + 1 + hlines

        l = 0
        if not self.graph_win_show:
            twin.attron(curses.color_pair(3))
            twin.addstr(l, 0, f"{'':▒>{self.columns}}")
            twin.attroff(curses.color_pair(3))
            l += 1

        if len(self.query.result) > 0:
            twin.attron(curses.color_pair(3))
            headerstr = '│' + '│'.join([f' {x:{self.query.width[i]}} ' for i, x in enumerate(self.query.columns)]) + '│'
            headerstr = f"{headerstr[self.cur_x: self.cur_x+self.columns-1]:{self.columns}}"
            twin.addstr(l, 0, headerstr)
            twin.attroff(curses.color_pair(3))
        else:
            twin.attron(curses.color_pair(3))
            twin.addstr(l, 0, f"{'':{self.columns}}")
            twin.attroff(curses.color_pair(3))
            l += 1
            twin.attron(curses.color_pair(2))
            s = " Empty resultset... "
            twin.addstr(l + ((self.table_win_lines - l) // 2) - 1, (self.columns - len(s)) // 2, s)
            twin.attroff(curses.color_pair(2))
        l += 1


        rows = [["" for _ in range(len(self.query.columns))] for _ in range(len(self.query.result))]
        for i, row in enumerate(self.query.result):
            for key, value in row.items():
                col_i = self.query.columns.index(key)
                rows[i][col_i] = str(value)

        for i, row in enumerate(rows[self.table_min:self.table_max]):
            if self.table_min + i == self.cur_y:
                twin.attron(curses.color_pair(2))

            ln = '│' + '│'.join([f' {x:{self.query.width[i]}} ' for i, x in enumerate(row)]) + '│'
            ln = f"{ln[self.cur_x:self.cur_x+self.columns-1]}"
            twin.addstr(i+l, 0, ln)

            if self.table_min + i == self.cur_y:
                twin.attroff(curses.color_pair(2))

    def _curses_graph_win(self, gwin):
        if self.query.graph_values is None:
            self.graph_win_show = False
        if self.graph_win_show and self.table_win_show:
            self.graph_win_lines = max(self.lines - self.table_win_lines - 1, 0)
        elif self.graph_win_show:
            self.graph_win_lines = self.lines - 1
        else: return

        gwin.resize(1,1)
        gwin.mvderwin(1, 0)
        gwin.resize(self.graph_win_lines, self.columns)

        fig = plotille.Figure()
        fig.width = max(self.columns - 22, 0)
        fig.height = max((self.graph_win_lines) - 9 - len(self.query.graph_data.keys()), 1)

        fig.color_mode = 'byte'
        fig.with_colors = True

        min_ = min([min((int(y[0]) for y in x), default=0) for x in self.query.graph_data.values()], default=0)
        max_ = max([max((int(y[0]) for y in x), default=3) for x in self.query.graph_data.values()], default=3)
        if min_ == max_: max_ += 1
        fig.set_x_limits(min_=min_, max_=max_)

        for label, data in self.query.graph_data.items():
            fig.plot(*zip(*data), label=label)

        legend = not ((len(self.query.graph_data) == 1) and (None in self.query.graph_data))
        out = fig.show(legend=legend)
        try:
            self.graph_win_cansi.addstr(out)
        except:
            pass

    def _watch(self):
        self.query.running = True
        query = self.query
        query.last_run = datetime.now()
        self.last_command_run_s = perf_counter()

        try:
            t1 = perf_counter()
            self.db.cur.execute(self.query.query)
            query.result = self.db.cur.fetchall()
            self.db.cnx.commit()
            query.execution_time = perf_counter() - t1
            self.query_had_error = False
        except Exception as e:
            self.query_error = str(e)
            self.query_had_error = True

        self.query.running = False
        self.screen_change_pending = True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H", type=str, help="database host [localhost]", default="127.0.0.1")
    parser.add_argument("--port", "-P", type=int, help="database port [3306]", default=3306)
    parser.add_argument("--user", "-u", type=str, help="database user", default=None)
    parser.add_argument("--database", "-d", type=str, help="database", default=None)
    parser.add_argument("--password", "-p", action="store_true", help="get database password from command line", default=False)

    parser.add_argument("--timeout", "-n", type=int, metavar='seconds', help="Update interval [2]", default=2)
    parser.add_argument("--graph-values", "-g", type=str, help="The column to use for graphing", default=None)
    parser.add_argument("--graph-column", "-c", type=str, help="The column to use for graphing labels", default=None)
    parser.add_argument("--graph-max-samples", type=int, help="How many samples to save before starting to scroll [1000]", default=1000)
    parser.add_argument("--vertical", "-v", action="store_true", help="Show rows vertically instead of in a table", default=False)

    parser.add_argument("query", metavar="QUERY", type=str, nargs="+", help="The query to watch")

    args = parser.parse_args()

    password = None
    if args.password:
        password = getpass("Password: ")

    query = QueryOptions(
        db_host = args.host,
        db_user = args.user,
        db_pass = password,
        db_base = args.database,
        db_port = args.port,
        query = " ".join(args.query),
        graph_values = args.graph_values,
        graph_labels = args.graph_column,
        graph_max_samples = args.graph_max_samples,
        vertical = args.vertical)


    watch_sql = WatchSQL(query, args.timeout, args.vertical)
    try:
        watch_sql.open_watch_curses()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()


