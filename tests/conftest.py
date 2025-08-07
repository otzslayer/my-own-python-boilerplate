import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def app() -> FastAPI:
    from main import app as actual_app

    return actual_app


@pytest.fixture(scope="session")
def client(app: FastAPI):
    with TestClient(app) as client:
        yield client
