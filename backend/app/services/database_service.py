# backend/app/services/database_service.py
# =================================================================
#
#                       Database Service
#
# =================================================================
#
#  Purpose:
#  --------
#  Provides a generic interface for interacting with the PostgreSQL
#  database (Neon). This service abstracts away the direct database
#  connection and query logic.
#
#  Key Features:
#  -------------
#  - Uses `psycopg2` for connecting to the PostgreSQL database.
#  - Manages a connection pool for efficient database access.
#  - Provides async-safe methods for data insertion and retrieval
#    using `asyncio.to_thread`.
#
# =================================================================

import asyncio
from contextlib import contextmanager

import psycopg2
from app.core.config import settings
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool


class DatabaseService:
    """
    Service for interacting with the PostgreSQL database.
    """

    _pool = None

    def __init__(self):
        if DatabaseService._pool is None:
            try:
                DatabaseService._pool = SimpleConnectionPool(
                    minconn=1, maxconn=10, dsn=settings.DATABASE_URL
                )
                print("Database connection pool created successfully.")
            except psycopg2.OperationalError as e:
                print(f"Error creating database connection pool: {e}")
                DatabaseService._pool = None  # Ensure pool is None if creation fails

    @contextmanager
    def _get_connection(self):
        """Context manager to get a connection from the pool."""
        if self._pool is None:
            raise ConnectionError("Database pool is not initialized.")

        conn = self._pool.getconn()
        try:
            yield conn
        finally:
            self._pool.putconn(conn)

    async def _execute_query(self, query, params=None, fetch=None):
        """Helper to run synchronous DB operations in a thread."""

        def db_op():
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, params)
                    if fetch == "one":
                        return cur.fetchone()
                    if fetch == "all":
                        return cur.fetchall()
                    conn.commit()
                    return None

        return await asyncio.to_thread(db_op)

    async def insert_data(self, table_name: str, data: dict):
        """
        Inserts a new record into the specified table.

        Note: This is a simplified and potentially unsafe implementation.
        For production, use a library that properly sanitizes inputs
        to prevent SQL injection.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = (
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING id"
        )

        try:
            result = await self._execute_query(query, tuple(data.values()), fetch="one")
            return result
        except Exception as e:
            print(f"Error inserting data: {e}")
            return None

    async def fetch_data(self, table_name: str, query_params: dict = None):
        """
        Fetches records from the specified table.
        """
        query = f"SELECT * FROM {table_name}"
        params = None
        if query_params:
            conditions = " AND ".join([f"{key} = %s" for key in query_params.keys()])
            query += f" WHERE {conditions}"
            params = tuple(query_params.values())

        try:
            return await self._execute_query(query, params, fetch="all")
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []


# Initialize a singleton instance
database_service = DatabaseService()
