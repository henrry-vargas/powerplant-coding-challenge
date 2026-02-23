from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_production_plan_payload1():
    payload_path = "example_payloads/payload1.json"
    with open(payload_path, "r") as f:
        payload = json.load(f)
    
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    total_p = sum(item["p"] for item in data)
    assert total_p == payload["load"]
    
    for item in data:
        name = item["name"]
        p_val = item["p"]
        plant = next(p for p in payload["powerplants"] if p["name"] == name)
        
        pmax = plant["pmax"]
        if plant["type"] == "windturbine":
            pmax = pmax * (payload["fuels"]["wind(%)"] / 100.0)
        
        if p_val > 0:
            assert p_val >= plant["pmin"]
            assert p_val <= pmax + 0.01
        else:
            assert p_val == 0

def test_production_plan_payload3():
    payload_path = "example_payloads/payload3.json"
    response_path = "example_payloads/response3.json"
    
    with open(payload_path, "r") as f:
        payload = json.load(f)
    with open(response_path, "r") as f:
        expected_response = json.load(f)
    
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    total_p = sum(item["p"] for item in data)
    assert total_p == payload["load"]
    
    expected_dict = {item["name"]: item["p"] for item in expected_response}
    actual_dict = {item["name"]: item["p"] for item in data}
    
    for name, p_val in expected_dict.items():
        assert actual_dict[name] == p_val
