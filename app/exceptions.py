from fastapi import HTTPException, status


class APIException(HTTPException):
    status_code = 500
    detail = "Internal Server Error"

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class OutOfStockException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Product out of stock"


class NotEnoughStockException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Requested quantity exceeds available stock"


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class IDNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "ID not found"


class SQLAlchemyException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "SQLAlchemy error"
