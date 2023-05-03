from typing import Any, Tuple

import psycopg2
from psycopg2.pool import ThreadedConnectionPool


class Cockroach:
    def __init__(self, url: str, _min: int, _max: int) -> None:
        self.cp = ThreadedConnectionPool(_min, _max, url)
    
    def get(self, query: str, params: Tuple[Any] = ()) -> str:
        res = None
        conn = self.cp.getconn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                res = cur.fetchall()
        self.cp.putconn(conn)
        return res
        
    def insert(self) -> bool:
        pass

    def test(self) -> str:
        return self.get("SELECT now()")

    def show_tables(self) -> str:
        return self.get("SHOW TABLES")
    
    def create_table(self, name: str, desc: str) -> bool:
        pass

    def delete_row(self, condition: str) -> bool:
        pass

    def close(self) -> None:
        self.cp.closeall()
