from app import app

def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_version():
    client = app.test_client()
    res = client.get("/version")
    assert res.status_code == 200

def test_predict_missing_text():
    client = app.test_client()
    res = client.post("/predict", json={})
    assert res.status_code == 400

def test_predict_valid():
    client = app.test_client()
    res = client.post("/predict", json={"text": "I love this"})
    assert res.status_code == 200
    body = res.get_json()
    assert "sentiment" in body
    assert "confidence" in body
