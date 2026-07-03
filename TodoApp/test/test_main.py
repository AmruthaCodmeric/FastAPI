#pip install httpx
#Test domain which is just checking to make sure that our application is healthy and change all of our application to have a root path(relative import)
from fastapi.testclient import TestClient
#import main
from ..main import app
from fastapi import status

client =TestClient(app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status':'Healthy'}