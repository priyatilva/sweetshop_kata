import unittest
from fastapi.testclient import TestClient
from main import app
import random
from database import Base, engine

# Reset DB for testing
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

class TestSweets(unittest.TestCase):

    def setUp(self):
        # ------------------------
        # Create normal user
        # ------------------------
        rand1 = random.randint(1, 10000)
        self.normal_user = f"user{rand1}"
        self.normal_email = f"{self.normal_user}@example.com"

        client.post("/api/auth/register", json={
            "username": self.normal_user,
            "email": self.normal_email,
            "password": "mypassword",
            "is_admin": 0
        })
        login_response = client.post("/api/auth/login", json={
            "username": self.normal_user,
            "password": "mypassword"
        })
        self.normal_token = login_response.json()["access_token"]

        # ------------------------
        # Create admin user
        # ------------------------
        rand2 = random.randint(1, 10000)
        self.admin_user = f"admin{rand2}"
        self.admin_email = f"{self.admin_user}@example.com"

        client.post("/api/auth/register", json={
            "username": self.admin_user,
            "email": self.admin_email,
            "password": "adminpassword",
            "is_admin": 1
        })
        login_response = client.post("/api/auth/login", json={
            "username": self.admin_user,
            "password": "adminpassword"
        })
        self.admin_token = login_response.json()["access_token"]

        # ------------------------
        # Create a sweet for all tests
        # ------------------------
        add_sweet_resp = client.post(
            "/api/sweets",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={
                "name": "Jalebi",
                "category": "Indian",
                "price": 12,
                "quantity": 40
            }
        )
        self.jalebi_id = add_sweet_resp.json()["id"]

    # ------------------------
    # Add Sweet Tests
    # ------------------------
    def test_add_sweet_requires_auth(self):
        response = client.post("/api/sweets", json={
            "name": "Ladoo",
            "category": "Indian",
            "price": 10,
            "quantity": 50
        })
        self.assertEqual(response.status_code, 401)

    def test_add_sweet_normal_user_forbidden(self):
        response = client.post(
            "/api/sweets",
            headers={"Authorization": f"Bearer {self.normal_token}"},
            json={
                "name": "GulabJamun",
                "category": "Indian",
                "price": 15,
                "quantity": 30
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_add_sweet_admin_success(self):
        response = client.post(
            "/api/sweets",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={
                "name": "Rasgulla",
                "category": "Indian",
                "price": 10,
                "quantity": 25
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Rasgulla")
        self.assertEqual(data["quantity"], 25)

    # ------------------------
    # List Sweets Tests
    # ------------------------
    def test_list_sweets_requires_auth(self):
        response = client.get("/api/sweets")
        self.assertEqual(response.status_code, 401)

    def test_list_sweets_user_success(self):
        response = client.get(
            "/api/sweets",
            headers={"Authorization": f"Bearer {self.normal_token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_list_sweets_admin_success(self):
        response = client.get(
            "/api/sweets",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    # ------------------------
    # Search Sweets Tests
    # ------------------------
    def test_search_sweets_requires_auth(self):
        response = client.get("/api/sweets/search?name=Jalebi")
        self.assertEqual(response.status_code, 401)

    def test_search_sweets_by_name_normal_user(self):
        response = client.get(
            f"/api/sweets/search?name=Jal",
            headers={"Authorization": f"Bearer {self.normal_token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Jalebi")

    def test_search_sweets_by_name_admin(self):
        response = client.get(
            f"/api/sweets/search?name=Jal",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Jalebi")

    # ------------------------
    # Update Sweet Tests
    # ------------------------
    def test_update_sweet_requires_auth(self):
        response = client.put(f"/api/sweets/{self.jalebi_id}", json={
            "name": "UpdatedLadoo",
            "category": "Indian",
            "price": 15,
            "quantity": 60
        })
        self.assertEqual(response.status_code, 401)

    def test_update_sweet_forbidden_for_non_admin(self):
        response = client.put(
            f"/api/sweets/{self.jalebi_id}",
            headers={"Authorization": f"Bearer {self.normal_token}"},
            json={
                "name": "JalebiUpdated",
                "category": "Indian",
                "price": 14,
                "quantity": 30
            }
        )
        self.assertEqual(response.status_code, 403)
        data = response.json()
        self.assertEqual(data["detail"], "Only admin users can update sweets")

    def test_update_sweet_success_for_admin(self):
        response = client.put(
            f"/api/sweets/{self.jalebi_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={
                "name": "JalebiUpdated",
                "category": "Indian",
                "price": 15,
                "quantity": 35
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "JalebiUpdated")
        self.assertEqual(data["price"], 15)
        self.assertEqual(data["quantity"], 35)

    # ------------------------
    # Delete Sweet Tests
    # ------------------------
    def test_delete_sweet_requires_auth(self):
        response = client.delete("/api/sweets/1")
        self.assertEqual(response.status_code, 401)
	    
    def test_delete_sweet_forbidden_for_non_admin(self):
        response = client.delete(
            f"/api/sweets/{self.jalebi_id}",
            headers={"Authorization": f"Bearer {self.normal_token}"}
        )
        self.assertEqual(response.status_code, 403)
        data = response.json()
        self.assertEqual(data["detail"], "Only admin users can delete sweets")

    def test_delete_sweet_success_for_admin(self):
        response = client.delete(
            f"/api/sweets/{self.jalebi_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["detail"], "Sweet deleted successfully")

# ------------------------
# Purchase Sweet Tests
# ------------------------
    def test_purchase_sweet_requires_auth(self):
        response = client.post(f"/api/sweets/{self.jalebi_id}/purchase", json={"quantity": 5})
        self.assertEqual(response.status_code, 401)

    def test_purchase_sweet_success(self):
        purchase_qty = 5
        # Get current quantity
        get_resp = client.get(
            f"/api/sweets",
            headers={"Authorization": f"Bearer {self.normal_token}"}
        )
        current_qty = next(s["quantity"] for s in get_resp.json() if s["id"] == self.jalebi_id)

        response = client.post(
            f"/api/sweets/{self.jalebi_id}/purchase",
            headers={"Authorization": f"Bearer {self.normal_token}"},
            json={"quantity": purchase_qty}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["quantity"], current_qty - purchase_qty)

    def test_purchase_sweet_insufficient_quantity(self):
        response = client.post(
            f"/api/sweets/{self.jalebi_id}/purchase",
            headers={"Authorization": f"Bearer {self.normal_token}"},
            json={"quantity": 50}  # More than available
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Not enough quantity available")


# ------------------------
# Restock Sweet Tests (Admin only)
# ------------------------
    def test_restock_sweet_requires_auth(self):
        response = client.post(f"/api/sweets/{self.jalebi_id}/restock", json={"quantity": 10})
        self.assertEqual(response.status_code, 401)

    def test_restock_sweet_forbidden_for_non_admin(self):
        response = client.post(
            f"/api/sweets/{self.jalebi_id}/restock",
            headers={"Authorization": f"Bearer {self.normal_token}"},
            json={"quantity": 10}
        )
        self.assertEqual(response.status_code, 403)

    def test_restock_sweet_success_for_admin(self):
        restock_qty = 10
        # Get current quantity
        get_resp = client.get(
            "/api/sweets",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        current_qty = next(s["quantity"] for s in get_resp.json() if s["id"] == self.jalebi_id)

        response = client.post(
            f"/api/sweets/{self.jalebi_id}/restock",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={"quantity": restock_qty}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["quantity"], current_qty + restock_qty)


if __name__ == "__main__":
    unittest.main()
