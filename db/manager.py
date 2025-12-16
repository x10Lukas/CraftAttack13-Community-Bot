import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "datenbank.db")

class Database:
    _connection = None

    @classmethod
    async def connect(cls):
        if cls._connection is None:
            cls._connection = await aiosqlite.connect(DB_PATH)
            await cls._connection.execute("PRAGMA foreign_keys = ON;")
        return cls._connection

    @classmethod
    async def close(cls):
        if cls._connection:
            await cls._connection.close()
            cls._connection = None

    @classmethod
    async def init_db(cls):
        db = await cls.connect()

        await db.executescript('''
            CREATE TABLE IF NOT EXISTS servers (
                ip TEXT NOT NULL,
                port INTEGER NOT NULL,
                display_name TEXT NOT NULL,
                PRIMARY KEY (ip, port)
            );
            
            CREATE TABLE IF NOT EXISTS status_messages (
                ip TEXT NOT NULL,
                port INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                display_name TEXT NOT NULL,
                PRIMARY KEY (ip, port)
            );
        ''')

        await db.commit()