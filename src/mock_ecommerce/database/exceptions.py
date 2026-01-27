"""
References: https://www.psycopg.org/docs/errors.html
"""

from mock_ecommerce.exceptions import EcommerceBaseError

class DatabaseError(EcommerceBaseError):
    """Base class for database exceptions."""
    pass

class DBConnectionError(DatabaseError):
    """Db connection error. (network, authentication)
        Transient -> retry
    """
    pass

class DBConstraintError(DatabaseError):
    """
        Dup ID, invalid values
        Permanent -> non-retry
    """
    pass

class DBOperationError(DatabaseError):
    """
        Syntax error
        Permanent -> non-retry (need code fixes)
    """
    pass
