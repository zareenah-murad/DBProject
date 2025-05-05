import pytest
from app import app, db

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Automatically reset tables before every test
@pytest.fixture(autouse=True)
def reset_tables():
    cursor = db.cursor()

    # Order matters due to foreign key constraints
    cursor.execute("DELETE FROM AnalysisResult")
    cursor.execute("DELETE FROM Posts")
    cursor.execute("DELETE FROM Users")
    cursor.execute("DELETE FROM SocialMedia")
    cursor.execute("DELETE FROM Field")
    cursor.execute("DELETE FROM Project")
    cursor.execute("DELETE FROM Institute")

    db.commit()