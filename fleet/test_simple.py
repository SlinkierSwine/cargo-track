#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")

def test_health():
    response = client.get("/health")
    print(f"Health endpoint: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_root()
    test_health() 