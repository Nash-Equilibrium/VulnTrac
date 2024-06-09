import unittest
from flask import Flask
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from dbTables import User
from init import db, app


class TestAuth(TestCase):

    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "mysql+pymysql://root:zyh20030827@localhost:3306/mydb"
        )
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        return app

    def setUp(self):
        db.create_all()

    def test_register(self):
        response = self.client.post(
            "/api/v1/register",
            json={
                "username": "testuser",
                "password": "testpassword",
                "email": "test@example.com",
                "role": "0",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

        user = User.query.filter_by(email="test@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_register_duplicate_email(self):
        user = User(
            username="testuser",
            password=generate_password_hash("testpassword"),
            email="test@example.com",
        )
        db.session.add(user)
        db.session.commit()

        response = self.client.post(
            "/api/v1/register",
            json={
                "username": "testuser2",
                "password": "testpassword2",
                "email": "test@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "error")
        self.assertEqual(response.json["message"], "Email already registered")

    def test_login(self):
        user = User(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )
        db.session.add(user)
        db.session.commit()

        response = self.client.post(
            "/api/v1/login", json={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["message"], "Login successful")

    def test_login_invalid_credentials(self):
        response = self.client.post(
            "/api/v1/login",
            json={"username": "invaliduser", "password": "invalidpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "error")
        self.assertEqual(response.json["message"], "Invalid username or password")

    def test_get_info(self):
        response = self.client.get("/api/v1/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["message"], "Get user info successful")
        self.assertEqual(response.json["data"]["username"], "admin")
        self.assertEqual(response.json["data"]["roles"], ["admin"])

    def test_logout(self):
        response = self.client.get("/api/v1/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["message"], "Logout successful")


if __name__ == "__main__":
    unittest.main()
