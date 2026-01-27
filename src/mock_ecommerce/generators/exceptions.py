from mock_ecommerce.exceptions import EcommerceBaseError

class GeneratorException(EcommerceBaseError):
    pass

class DataValidationError(GeneratorException):
    pass
