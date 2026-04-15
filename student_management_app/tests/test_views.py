"""
Tests for the application views.
"""

from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from student_management_app.models import (
    Courses,
    CustomUser,
    SessionYearModel,
    Staffs,
    Students,
)


class LoginViewTest(TestCase):
    """Test cases for login views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            user_type=1,
        )

    def test_login_page_loads(self):
        """Test that the login page loads successfully."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        """Test login with valid credentials."""
        response = self.client.post(
            reverse("doLogin"),
            {"email": "test@example.com", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 302)

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(
            reverse("doLogin"),
            {"email": "test@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 302)


class HODViewsTest(TestCase):
    """Test cases for HOD views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.session = SessionYearModel.objects.create(
            session_start_year=date(2024, 1, 1),
            session_end_year=date(2024, 12, 31),
        )
        self.hod_user = CustomUser.objects.create_user(
            username="hod_test",
            email="hod@test.com",
            password="testpass123",
            user_type=1,
        )

    def test_admin_home_requires_login(self):
        """Test that admin home requires login."""
        response = self.client.get(reverse("admin_home"))
        self.assertEqual(response.status_code, 302)

    def test_add_staff_requires_login(self):
        """Test that add staff page requires login."""
        response = self.client.get(reverse("add_staff"))
        self.assertEqual(response.status_code, 302)


class StaffViewsTest(TestCase):
    """Test cases for Staff views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.session = SessionYearModel.objects.create(
            session_start_year=date(2024, 1, 1),
            session_end_year=date(2024, 12, 31),
        )
        self.course = Courses.objects.create(course_name="Computer Science")
        self.staff_user = CustomUser.objects.create_user(
            username="staff_test",
            email="staff@test.com",
            password="testpass123",
            user_type=2,
        )

    def test_staff_home_requires_login(self):
        """Test that staff home requires login."""
        response = self.client.get(reverse("staff_home"))
        self.assertEqual(response.status_code, 302)


class StudentViewsTest(TestCase):
    """Test cases for Student views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.session = SessionYearModel.objects.create(
            session_start_year=date(2024, 1, 1),
            session_end_year=date(2024, 12, 31),
        )
        self.course = Courses.objects.create(course_name="Computer Science")
        self.student_user = CustomUser.objects.create_user(
            username="student_test",
            email="student@test.com",
            password="testpass123",
            user_type=3,
        )

    def test_student_home_requires_login(self):
        """Test that student home requires login."""
        response = self.client.get(reverse("student_home"))
        self.assertEqual(response.status_code, 302)


class LogoutViewTest(TestCase):
    """Test cases for logout view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            user_type=1,
        )

    def test_logout(self):
        """Test logout functionality."""
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("logout_user"))
        self.assertEqual(response.status_code, 302)
