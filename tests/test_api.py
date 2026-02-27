import json
from app import app

def test_candidate_api():
    client = app.test_client()

    data = {
        "candidate": {"full_name": "Test User", "summary": "Developer", "years_experience": 2},
        "contacts": {"email": "test@test.com"},
        "skills": [{"skill_name": "Python", "category": "technical"}],
        "education": [],
        "experience": []
    }

    response = client.post("/api/v1/candidate",
                           data=json.dumps(data),
                           content_type="application/json")

    assert response.status_code in [200,201]
