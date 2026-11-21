from fastapi.testclient import TestClient

from steamrec.api import app

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json()["status"] == "ok"


def test_analyze_defaults():
    r = client.post("/api/analyze", json={})
    assert r.status_code == 200
    body = r.json()
    assert body["economics"]["net_benefit_usd"] > 0
    assert len(body["sensitivity"]["curves"]) == 3


def test_analyze_bad_input():
    r = client.post("/api/analyze", json={"hw_supply_F": 100, "hw_return_F": 120})
    assert r.status_code == 422


def test_frontend_served():
    r = client.get("/")
    assert r.status_code == 200
    assert "Waste Steam Recovery" in r.text
