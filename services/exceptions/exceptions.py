from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


class TransactionError(Exception):
    def __init__(self, message: str = "Insufficient funds to complete the transaction"):
        self.message = message
        super().__init__(self.message)


class ExceptionHandler:

    @staticmethod
    def handle(e: Exception):
        match e:
            case HTTPException():
                print(e, "HTTPException")
                raise e
            case NotImplementedError() as e:
                print(e, "NotImplementedError")
                raise HTTPException(
                    status_code=status.HTTP_501_NOT_IMPLEMENTED,
                    detail=e.message
                )
            case SQLAlchemyError():
                print(e, "SQLAlchemyError")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error occurred"
                )
            case TransactionError() as insufficient_funds_err:
                print(insufficient_funds_err, "Insufficient funds")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=insufficient_funds_err.message
                )
            case ConnectionError() as conn_err:
                print(e, "ConnectionError")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=conn_err.args[0]
                )
            case _:
                print(e, "Unknown error")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred"
                )
