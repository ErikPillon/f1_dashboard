import pytest
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture()
def db_engine():
    return create_engine(DATABASE_URL)
