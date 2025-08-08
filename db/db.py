import enum
import sqlite3
from pathlib import Path
from typing import Any, List, Dict

import paths


class DbName(enum.StrEnum):
    USERS = "users"


class ObDB:
    def __init__(
            self,
            db_name: DbName,
            path: Path = paths.DATA_DIR
    ):
        self.__db_name = db_name
        self.__path = path / f"{db_name}.db"

        self.__conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def __enter__(self):
        if self.__conn is not None:
            raise TypeError(f"{self.__db_name} already connected in this ObDB instance.")
        self.__conn = sqlite3.connect(self.__path)
        self.cursor = self.__conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__conn is None:
            raise TypeError(f"Tried to close {self.__db_name} before connecting to it.")
        if self.cursor is not None:
            self.cursor.close()
        self.__conn.commit()
        self.__conn.close()

    def __getattribute__(self, item):
        if item == "cursor" and self.__conn is None:
            raise TypeError(f"Cannot use ObDB outside of a 'with' block.")
        return super().__getattribute__(item)

    def create_table(
            self,
            *sqlite_lines: str
    ):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.__db_name} ({','.join(sqlite_lines)});")

    def upsert(
            self,
            id: str | int,
            **kv_pairs: Any
    ):
        id = str(id)
        query = f"""
            INSERT INTO {self.__db_name} (id, {", ".join(kv_pairs.keys())}) 
            VALUES ({", ".join(['?'] * (1 + len(kv_pairs)))})
            ON CONFLICT(id) DO UPDATE SET {", ".join(f"{key}=excluded.{key}" for key in kv_pairs.keys())};
        """
        values = (id, *kv_pairs.values())
        self.cursor.execute(query, values)

    def read(
            self,
            id: str | int,
            *cols: str,
            fetch_all: bool = False
    ) -> Any | List[Any] | Dict[str, Any] | List[Dict[str, Any]] | None:
        id = str(id)
        query = f"""
            SELECT {", ".join(cols)}
            FROM {self.__db_name}
            WHERE id = ?;
        """
        values = (id,)
        self.cursor.execute(query, values)
        if fetch_all:
            result = self.cursor.fetchall()
            if result is not None and len(cols) == 1:
                return [r[0] for r in result]
            return result
        else:
            result = self.cursor.fetchone()
            if result is not None and len(cols) == 1:
                return result[0]
            return result
