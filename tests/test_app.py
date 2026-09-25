from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get("/health").json()["status"]=="ok"
def test_create_case(): r=client.post("/cases",json={"title":"Lab Incident"}); assert r.status_code==200; assert r.json()["title"]=="Lab Incident"