from fastapi import HTTPException, status


class APIException(HTTPException):
    status_code = 500
    detail = "Внутренняя ошибка сервера"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class OutOfStockException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Товара нет в наличии"


class NotEnoughStockException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Запрашиваемое количество товара превышает количество на складе"


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Ничего не найдено"


class IDNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "ID не найден"


class SQLAlchemyException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка ORM SQLAlchemy"
