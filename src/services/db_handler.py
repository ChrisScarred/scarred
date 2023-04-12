import psycopg2

class Cockroach:
    def __init__(self, url: str) -> None:
        self.connection = psycopg2.connect(url)
    
    def test(self) -> str:
        with self.connection.cursor() as cur:
            cur.execute("SELECT now()")
            res = cur.fetchall()
            self.connection.commit()
            return res
