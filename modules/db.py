import sqlite3
import random
import time

from datetime import datetime


class BaseDB:
    def __init__(self):
        pass

    def db_create_connection(self, db_file='db.sqlite3'):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f'- Connected to db')
        except Exception as e:
            print(e)
        return conn

    def db_create_table(self, conn, sql):
        try:
            cur = conn.cursor()
            cur.execute(sql)
        except Exception as e:
            print(e)

    def db_create_tables(self, db_conn):
        if db_conn:
            self.db_create_table(
                db_conn, self.sql_create_trade_users_table)
            self.db_create_table(
                db_conn, self.sql_create_ignored_users_table)
        else:
            print(f"- Error! Cannot connect to db. {db_conn}")
            return False

    def db_create_object(self, conn, sql, data):
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

    def db_update_object(self, conn, sql, data):
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

    def db_delete_object(self, conn, table, column, value):
        sql = f'DELETE FROM {table} WHERE {column}=?'
        cur = conn.cursor()
        cur.execute(sql, (value,))
        conn.commit()

    def db_flush_objects(self, conn, table):
        sql = f'DELETE FROM {table}'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def db_get_all(self, conn, table):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()

    def db_get_object(self, conn, table, column, value):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {table} WHERE {column}=?', (value,))
        return cur.fetchone()

    def db_get_latest_objects(self, db_conn, table, column, amount=10, latest=0):
        cur = db_conn.cursor()
        cur.execute(f'SELECT * FROM {table} ORDER BY {column} DESC')
        if latest:
            fmt = '%Y-%m-%d %H:%M:%S'
            rows = set()
            for row in cur:
                time_now = str(datetime.now())
                time_now_strp = datetime.strptime(time_now.split('.')[0], fmt)
                last_whisper_strp = datetime.strptime(
                    row[7].split('.')[0], fmt)
                last_whisper_raw = time_now_strp - last_whisper_strp
                last_whisper_sec = int(last_whisper_raw.total_seconds())
                if last_whisper_sec <= latest:
                    rows.add(row)
            return sorted(rows)
        else:
            return cur.fetchall()[:amount]


class TradeDB(BaseDB):
    def __init__(self):
        self.sql_create_trade_users_table = """
            CREATE TABLE IF NOT EXISTS trade_users (
                id integer PRIMARY KEY,
                acc_name text NOT NULL UNIQUE,
                char_name text NOT NULL,
                item_type text NOT NULL,
                item_id text NOT NULL,
                item_name text NOT NULL,
                item_price integer NOT NULL,
                item_amount integer NOT NULL,
                item_currency text NOT NULL,
                last_trade text NOT NULL,
                priority integer DEFAULT 10,
                trade_attempts integer DEFAULT 3
            );"""
        self.sql_create_ignored_users_table = """
            CREATE TABLE IF NOT EXISTS ignored_users (
                id integer PRIMARY KEY,
                acc_name text NOT NULL UNIQUE,
                created text NOT NULL
            );"""
        self.sql_create_trade_items_table = """
            CREATE TABLE IF NOT EXISTS trade_items (
                id integer PRIMARY KEY,
                item_id text NOT NULL UNIQUE,
                item_type text NOT NULL,
                buyout_currency text NOT NULL,
                min_price integer NOT NULL,
                max_price integer NOT NULL,
                min_stock_amount integer NOT NULL,
                max_stock_price integer NOT NULL,
                disabled boolean NOT NULL,
            );"""
        self.sql_create_prices_table = """
            CREATE TABLE IF NOT EXISTS prices (
                id integer PRIMARY KEY,
                item_id text NOT NULL UNIQUE,
                item_quantity integer NOT NULL,
                item_tendency text,
                item_tendency_pc integer DEFAULT 0,
                item_avg_price integer NOT NULL,
                last_avg_price integer DEFAULT 0,
                poeninja_price integer DEFAULT 0,
                last_update text NOT NULL,
            );"""
        self.sql_insert_trade_user = """
            INSERT INTO trade_users(
                    acc_name,
                    char_name,
                    item_type,
                    item_id,
                    item_name,
                    item_price,
                    item_amount,
                    item_currency,
                    last_trade
                )
                VALUES(?,?,?,?,?,?,?,?,?)
            """
        self.sql_insert_ignored_user = """
            INSERT OR REPLACE INTO ignored_users(
                    acc_name,
                    created
                )
                VALUES(?,?)
            """
        self.sql_insert_trade_item = """
            INSERT INTO trade_items(
                    item_id,
                    item_type,
                    buyout_currency,
                    min_price,
                    max_price,
                    min_stock_amount,
                    max_stock_price,
                    disabled
                )
                VALUES(?,?,?,?,?,?,?,?)
            """
        self.sql_insert_price = """
            INSERT INTO prices(
                    item_id,
                    item_quantity,
                    item_tendency,
                    item_tendency_pc,
                    item_avg_price,
                    last_avg_price,
                    poeninja_price,
                    last_update
                )
                VALUES(?,?,?,?,?,?,?,?)
            """
        self.sql_update_trade_user = """
            UPDATE trade_users
                SET char_name = ?,
                    item_type = ?,
                    item_id = ?,
                    item_name = ?,
                    item_price = ?,
                    item_amount = ?,
                    item_currency = ?
                WHERE acc_name = ?
            """
        self.sql_update_trade_user_priority = """
            UPDATE trade_users
                SET last_trade = ?,
                    priority = ?,
                    trade_attempts = ?
                WHERE acc_name = ?
            """
        self.sql_upsert_prices = """
            INSERT INTO prices (item_id,)
            VALUES (item_id,), (item_id,)
            ON CONFLICT (item_id) DO UPDATE
            SET column_1 = excluded.column_1,
                column_2 = excluded.column_2;
        """

    def db_update_trade_user_priority(self, db_conn, trade_user, updated_at):
        """Update DB user last_trade/priority/attempts"""
        attempts = trade_user[-1] - 1 if trade_user[-1] else 3
        priority = trade_user[-2] - 1 if not trade_user[-1] else trade_user[-2]
        filepath = 'temp/ignored_accounts.txt'
        if not priority:
            with open(filepath, 'a', encoding='utf-8') as ignored_users:
                ignored_users.write(trade_user[1] + '\n')
            self.db_insert_new_ignored_users(db_conn)
        self.db_update_object(
            db_conn,
            self.sql_update_trade_user_priority,
            (updated_at, priority, attempts, trade_user[1])
        )

    def db_insert_default_ignored_users(self, db_conn):
        ignored_users = self.db_get_all(db_conn, 'ignored_users')
        filepath = 'temp/ignored_accounts.txt'
        if not ignored_users:
            try:
                with open(filepath, "r", encoding="utf8") as ignored_users:
                    for user in ignored_users:
                        user = str(user).strip().lower()
                        user_data = (
                            user,
                            str(datetime.now()),
                        )
                        with db_conn:
                            self.db_create_object(
                                db_conn,
                                self.sql_insert_ignored_user,
                                user_data)
                        print(f'- Added default_ignored_user: {user}')
            except FileNotFoundError:
                with open(filepath, 'w+') as file:
                    file.write('')
        return ignored_users

    def db_insert_new_ignored_users(self, db_conn):
        """
        TODO: Fix init db
              ValueError: I/O operation on closed file.
        """
        time.sleep(random.uniform(0.1, 0.3))  # prevent concurrent unique
        with open("temp/ignored_accounts.txt", "r", encoding="utf8") as ignored_users:
            for user in ignored_users:
                user = user.strip().lower()
                account_ignored = [i for i in self.trade_ignored_users if user in i]
                if not account_ignored:
                    user_data = (
                        user,
                        str(datetime.now()),
                    )
                    with db_conn:
                        self.db_create_object(
                            db_conn,
                            self.sql_insert_ignored_user,
                            user_data)
                    self.trade_ignored_users = self.db_get_all(db_conn, 'ignored_users')
                    print(f'- New ignored_user added: {user}')
