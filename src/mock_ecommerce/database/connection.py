import psycopg2
from psycopg2 import OperationalError, InterfaceError
from mock_ecommerce.config import settings
from mock_ecommerce.utils.logger import logger
from mock_ecommerce.database.exceptions import (
    DBConnectionError,
    DatabaseError
)

def get_db_connection():
    """
    Create a connection to the PostgreSQL database
    TODO: Context Manager ? Connection Pool ?
    """
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        logger.info(f'Connected to {settings.DATABASE_URL}')
        return conn
    except (InterfaceError, OperationalError) as e:
        logger.exception(f'Connection failed: {e}')
        raise DBConnectionError('Could not connect to PostgreSQL database', original_exception=e)
    except Exception as e:
        logger.error(f'Unexpected DB error: {e}')
        raise DatabaseError('Unexpected error', original_exception=e)
