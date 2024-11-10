import sqlite3


class SQLite:

    def __init__(self, db_file, table_sql):
        self.db_file = db_file
        self.conn = self.create_connection()
        self.table_sql = table_sql
        self.create_table(table_sql=self.table_sql)

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Exception as e:
            print(e)

        return conn

    def create_table(self, table_sql):
        if self.conn is not None:
            c = self.conn.cursor()
            c.execute(table_sql)
            self.conn.commit()

    def check_content_exists(self, content):
        c = self.conn.cursor()
        c.execute("SELECT * FROM texts WHERE content = ?", (content,))
        return c.fetchone() is not None

    def insert_content(self, content):
        c = self.conn.cursor()

        if not self.check_content_exists(content):
            c.execute("INSERT INTO texts (content) VALUES (?)", (content,))
            self.conn.commit()
            # print("内容已插入")

    def close_connection(self):
        if self.conn:
            self.conn.close()

    # 可选：使用析构函数（但请注意，它可能不会被调用）
    def __del__(self):
        self.close_connection()


if __name__ == "__main__":
    db_file = "./data/sqlite.db"
    table_sql = """CREATE TABLE IF NOT EXISTS texts
                (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)"""
    db = SQLite(db_file, table_sql)
    print(db.check_content_exists("test"))
    db.insert_content("test")
    print("test inserted")
    print(db.check_content_exists("test"))
    db.close_connection()
