import sqlite3
import asyncio

conn = sqlite3.connect('info.db', timeout=5.0)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS weapons (
                weaponName TEXT PRIMARY KEY,
                weaponType TEXT,
                secondaryStats TEXT,
                baseAttackRange TEXT,
                secondaryRange TEXT,
                weaponStats TEXT,
                effectName TEXT,
                effectDescription TEXT,
                imageLink TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS characters (
                characterName TEXT PRIMARY KEY,
                wikiLink TEXT,
                imageLink TEXT,
                rarityLevel TEXT,
                weaponType TEXT,
                characterVision TEXT,
                characterStats TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS artifacts (
                setName TEXT PRIMARY KEY,
                artifactOrigin TEXT,
                imageLink TEXT,
                wikiLink TEXT,
                setEffect TEXT)''')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database:
    @staticmethod
    def connect():
        conn = sqlite3.connect('info.db', timeout=5.0, check_same_thread=False)
        c = conn.cursor()
        return c

    @staticmethod
    async def execute(statement, *args):
        loop = asyncio.get_event_loop()
        c = Database.connect()
        await loop.run_in_executor(None, lambda: c.execute(statement, args))
        c.connection.commit()
        c.connection.close()

    @staticmethod
    def get(statement, *args):
        c = Database.connect()
        c.row_factory = dict_factory
        res = c.execute(statement, args).fetchall()
        c.connection.close()
        return res
