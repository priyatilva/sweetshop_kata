import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAuth(unittest.TestCase):

    def test_register_user(self):
        response = client.post(
            "/api/auth/register",
            json={"username": "priya1", "email": "priya1@example.com", "password": "mypassword1"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "priya1")
        self.assertEqual(data["email"], "priya1@example.com")
        self.assertIn("id", data)

    def test_login_user(self):
        # Register a new user specifically for login test
        client.post(
            "/api/auth/register",
            json={"username": "loginuser1", "email": "login1@example.com", "password": "mypassword1"}
        )

        # Now login with that user
        response = client.post(
            "/api/auth/login",
            json={"username": "loginuser1", "password": "mypassword1"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")

if __name__ == "__main__":
    unittest.main()
