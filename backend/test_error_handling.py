from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def simulate_failure(question):
    raise RuntimeError("Simulated internal service failure")


with patch("main.answer_question", side_effect=simulate_failure):
    response = client.post(
        "/chat",
        json={"question": "Test error handling"}
    )

print("Status Code:", response.status_code)
print("Response:", response.json())

assert response.status_code == 500

assert response.json() == {
    "detail": "Unable to process the request. Please try again later."
}

print("Error handling test PASSED")