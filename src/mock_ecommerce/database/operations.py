from typing import List, Dict, Any
from psycopg2.extras import execute_values
from psycopg2 import IntegrityError, OperationalError

from mock_ecommerce.database.connection import get_db_connection
from mock_ecommerce.utils.logger import logger
from mock_ecommerce.database.ddl import get_ddl_statements
from mock_ecommerce.database.exceptions import (
    DBOperationError,
    DBConstraintError,
    DBConnectionError,
    DatabaseError
)

# Global cache for FK refer
_CACHE_FK_ID: Dict[str, List[int]] = {}

def execute_query(query: str, params: tuple = None) -> None:
    """
    Execute an SQL statement
    """
    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
            logger.debug(f"Executed query: {query[:50]}...")

        except Exception as e:
            raise DBOperationError(f"Failed to execute query: {query[:50]}", original_exception=e)

def validate_tables_exist(required_tables: List[str]) -> bool:
    """
    Check if tables exist
    """
    check_sql = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public' \
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(check_sql)
            # Set comprehension: {'brand', 'product', ...}
            existing_tables = {row[0] for row in cur.fetchall()}
            logger.info(f"Existing tables: {existing_tables}")
    missing = [t for t in required_tables if t not in existing_tables]

    if missing:
        logger.error(f"Missing required tables: {missing}")
        return False

    logger.info("Schema validation passed.")
    return True


def create_all_tables() -> None:
    logger.info("Initializing Database Schema...")
    statements = get_ddl_statements()

    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                for stmt in statements:
                    if stmt.strip():
                        cur.execute(stmt)
            conn.commit()
            logger.info("All tables created successfully.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Schema creation failed: {e}")
            raise DBOperationError("Schema creation failed", original_exception=e)


def bulk_insert(table_name: str, records: List[Dict[str, Any]]) -> int:
    """
    Insert a dictionary into the table
    """
    if not records:
        return 0

    # --- Get columns list from the 1st record ---
    columns = list(records[0].keys())

    # --- Create query template ---
    cols_str = ",".join(columns)
    query = f'INSERT INTO "{table_name}" ({cols_str}) VALUES %s'

    # --- Prepare & send data ---
    values = [tuple(r.values()) for r in records]
    inserted_count = 0

    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                execute_values(cur, query, values, page_size=1000) # send in batch
                inserted_count = len(values)
            conn.commit()
            logger.info(f"Inserted {inserted_count} rows into '{table_name}'")

        except IntegrityError as e:
            logger.error(f"Data error in '{table_name}': {e}")
            conn.rollback()
            raise DBConstraintError("Data constraint violated", original_exception=e)

        except OperationalError as e:
            logger.error(f"Connection lost during insert '{table_name}': {e}")
            conn.rollback()
            raise DBConnectionError("Connection lost during insert", original_exception=e)

        except Exception as e:
            logger.error(f"Unexpected error in '{table_name}': {e}")
            conn.rollback()
            raise DatabaseError("Bulk insert failed", original_exception=e)

    return inserted_count


def get_existing_ids(table_name: str, id_column: str, force_refresh: bool = False) -> List[int]:
    """
    Get IDs from db & cache on RAM for faster FK Sampling.
    """
    cache_key = f"{table_name}.{id_column}"

    # --- Return cache if exist ----
    if not force_refresh and cache_key in _CACHE_FK_ID:
        return _CACHE_FK_ID[cache_key][:]

    # --- else: fetch from db ---
    logger.debug(f"Fetching IDs for {cache_key}...")
    ids = []
    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                query = f'SELECT "{id_column}" FROM "{table_name}"'
                cur.execute(query)
                ids = [row[0] for row in cur.fetchall()]

        except Exception as e:
            logger.error(f"Failed to fetch IDs from {table_name}: {e}")
            raise DBOperationError(f"Fetch IDs failed for {table_name}", original_exception=e)

    # --- save to cache ----
    _CACHE_FK_ID[cache_key] = ids
    logger.info(f"Cached {len(ids)} IDs from {table_name}.{id_column}. Cache: {_CACHE_FK_ID}")
    return ids
