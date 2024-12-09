import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from services.exceptions.exceptions import ExceptionHandler, TransactionError

app = FastAPI()

@app.get("/raise_http_exception")
def raise_http_exception():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

@app.get("/raise_sqlalchemy_error")
def raise_sqlalchemy_error():
    try:
        raise SQLAlchemyError("Database connection failed")
    except Exception as e:
        ExceptionHandler.handle(e)

@app.get("/raise_transaction_error")
def raise_transaction_error():
    try:
        raise TransactionError("Insufficient funds to process this transaction")
    except Exception as e:
        ExceptionHandler.handle(e)

@app.get("/raise_connection_error")
def raise_connection_error():
    try:
        raise ConnectionError("Unable to connect to the blockchain node")
    except Exception as e:
        ExceptionHandler.handle(e)

@app.get("/raise_unknown_error")
def raise_unknown_error():
    try:
        raise ValueError("Some unexpected error")
    except Exception as e:
        ExceptionHandler.handle(e)

client = TestClient(app)

# tests
def test_http_exception():
    response = client.get("/raise_http_exception")
    assert response.status_code == 404
    assert response.json() == {"detail": "Resource not found"}

def test_sqlalchemy_error():
    response = client.get("/raise_sqlalchemy_error")
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error occurred"}

def test_transaction_error():
    response = client.get("/raise_transaction_error")
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient funds to process this transaction"}

def test_connection_error():
    response = client.get("/raise_connection_error")
    assert response.status_code == 500
    assert response.json() == {"detail": "Unable to connect to the blockchain node"}

def test_unknown_error():
    response = client.get("/raise_unknown_error")
    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred"}
