from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rank_resume_partial_match():
    payload = {
        "resume": "I have experience in Python and data analysis.",
        "job": "Looking for a candidate skilled in Python, SQL, and machine learning."
    }
    response = client.post("/rank_resume", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert data["score"] > 0
    assert "python" in data["found_keywords"]
    assert "sql" in data["missing_keywords"]

def test_rank_resume_all_keywords_found():
    payload = {
        "resume": "Python SQL machine learning",
        "job": "Python SQL machine learning"
    }
    response = client.post("/rank_resume", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 100
    assert len(data["missing_keywords"]) == 0

def test_rank_resume_no_keywords_found():
    payload = {
        "resume": "I like painting and swimming.",
        "job": "Python SQL machine learning"
    }
    response = client.post("/rank_resume", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 0
    assert len(data["found_keywords"]) == 0

def test_rank_resume_empty_fields():
    payload = {
        "resume": "",
        "job": ""
    }
    response = client.post("/rank_resume", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 0
    assert isinstance(data["found_keywords"], list)
    assert isinstance(data["missing_keywords"], list)

def test_rank_resume_with_non_ascii_characters():
    payload = {
        "resume": "Python 🐍 data analysis 🚀",
        "job": "Python and data analysis"
    }
    response = client.post("/rank_resume", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] > 0
    assert "python" in data["found_keywords"]