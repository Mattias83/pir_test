import sqlite3

from typing import Optional


class Connection:
    def __init__(self, db_location: str) -> None:
        self.db_location = db_location
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Cursor:
        self.conn = sqlite3.connect(self.db_location)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        traceback: Optional[object],
    ) -> None:
        if self.conn:
            self.conn.commit()
            self.conn.close()
