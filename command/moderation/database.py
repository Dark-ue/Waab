import sqlite3
import os
import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                            user_id INTEGER,
                            count INTEGER,
                            timestamp DATETIME,
                            guild_id INTEGER,
                            PRIMARY KEY (user_id, timestamp)
                        )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS settings (
                            guild_id INTEGER PRIMARY KEY,
                            warn_deletion_period INTEGER DEFAULT 10
                        )''')
        self.conn.commit()

    def get_warnings(self, user_id):
        self.c.execute('SELECT count FROM warnings WHERE user_id = ?', (user_id,))
        result = self.c.fetchall()
        return sum([row[0] for row in result])

    def add_warning(self, user_id, guild_id):
        timestamp = datetime.datetime.now()
        self.c.execute('INSERT INTO warnings (user_id, count, timestamp, guild_id) VALUES (?, ?, ?, ?)', (user_id, 1, timestamp, guild_id))
        self.conn.commit()

    def delete_expired_warnings(self, guild_id):
        self.c.execute('SELECT warn_deletion_period FROM settings WHERE guild_id = ?', (guild_id,))
        result = self.c.fetchone()
        if result:
            expiration_days = result[0]
        else:
            expiration_days = 10  # Default to 10 days if no setting is found
        expiration_date = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
        self.c.execute('DELETE FROM warnings WHERE timestamp < ? AND guild_id = ?', (expiration_date, guild_id))
        self.conn.commit()

    def set_warn_deletion_period(self, guild_id, days):
        self.c.execute('INSERT OR REPLACE INTO settings (guild_id, warn_deletion_period) VALUES (?, ?)', (guild_id, days))
        self.conn.commit()

    def close(self):
        self.conn.close()