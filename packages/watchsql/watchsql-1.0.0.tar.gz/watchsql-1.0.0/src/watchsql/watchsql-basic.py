import argparse
import MySQLdb
import MySQLdb.cursors
from getpass import getpass
from dataclasses import dataclass

import os
from time import sleep
from datetime import datetime
from time import perf_counter

@dataclass
class QueryOptions:
    db_host: str
    db_user: str | None
    db_pass: str | None
    db_base: str | None
    query: str
    graphs: str

class AltBuffer:
    def __enter__(self): print("\u001b[?47h")
    def __exit__(self, *args):
        print("", flush=True)
        print("\u001b[?47l")

class DBConnection:
    """ Context manager, that CAN be used "manually" with the open and close methods. """

    def __init__(self, queryOptions: QueryOptions, cursorclass=MySQLdb.cursors.DictCursor, **params):
        self.cursorclass = cursorclass
        self.connect_params = {
            "host": queryOptions.db_host,
            "user": queryOptions.db_user,
            "passwd": queryOptions.db_pass,
            "db": queryOptions.db_base,
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

def print_table(data):
    columns = []
    for row in data:
        for key in row.keys():
            if key not in columns:
                columns.append(key)
    width = [len(x) for x in columns]

    rows = [[None for _ in range(len(columns))] for _ in range(len(data))]
    for i, row in enumerate(data):
        for key, value in row.items():
            col_i = columns.index(key)
            #rows[i][columns.index(key)] = str(value) if type(value) is not bytes else value.decode("UTF-8")
            rows[i][col_i] = str(value)
            if value is not None:
                width[col_i] = max(width[col_i], len(str(value)))

    out =  f"+{'+'.join(['-' * (x+2) for x in width])}+\n"
    out += f"|{'|'.join([f' {x:{width[i]}} ' for i, x in enumerate(columns)])}|\n"
    out +=  f"+{'+'.join(['-' * (x+2) for x in width])}+\n"

    for row in rows:
        out += f"|{'|'.join([f' {x:{width[i]}} ' for i, x in enumerate(row)])}|\n"

    out +=  f"+{'+'.join(['-' * (x+2) for x in width])}+\n"

    size = os.get_terminal_size()
    out = "\n".join([x if len(x) < size.columns else x[:size.columns] for x in out.split("\n")])
    if out.count("\n") > size.lines-2: out = "\n".join(out.split("\n")[:size.lines-2])
    print(out)

def print_table_vertical(data):
    margin = max(max([len(y) for y in x.keys()]) for x in data)
    out = ""
    for i, row in enumerate(data):
        out += f"*************************** {i}. row ***************************\n"
        for key, value in row.items():
            out += f"{key:>{margin}}: {value}\n"

    size = os.get_terminal_size()
    out = "\n".join([x if len(x) < size.columns else x[:size.columns] for x in out.split("\n")])
    if out.count("\n") > size.lines-2: out = "\n".join(out.split("\n")[:size.lines-2])
    print(out)

def titlebar(running, time=None):
    size = os.get_terminal_size()
    print("\u001b[2J\u001b[0d\u001b[0H\u001b[7m", end="")

    text = f"{datetime.now()}: "
    if running:
        text += "Query running..."
    else:
        text += f" in {time:6.2f} s"

    print(text, end=" " * (size.columns - len(text)))
    print("\u001b[0m")

def watch_query(query: QueryOptions, timeout: int, vertical_table: bool):
    db = DBConnection(query)
    db.open()

    last_update = perf_counter()
    while True:
        titlebar(True)

        t1 = perf_counter()
        db.cur.execute(query.query)
        res = db.cur.fetchall()
        time = perf_counter() - t1
        titlebar(False, time)

        if vertical_table:
            print_table_vertical(res)
        else:
            print_table(res)

        sleep(timeout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H", type=str, help="database host", default="localhost")
    parser.add_argument("--user", "-u", type=str, help="database user", default=None)
    parser.add_argument("--database", "-d", type=str, help="database", default=None)
    parser.add_argument("--password", "-p", action="store_true", help="get database password from command line", default=False)

    parser.add_argument("--timeout", "-n", type=int, metavar='seconds', help="Update interval", default=2)
    parser.add_argument("--graph", "-g", type=str, nargs="+", help="The query keys to graph")
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
        query = " ".join(args.query),
        graphs = args.graph)

    with AltBuffer():
        watch_query(query, args.timeout, args.vertical)


