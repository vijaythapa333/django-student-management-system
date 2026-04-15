"""
Tests for the application models.
"""

from datetime import date

from django.test import TestCase

from student_management_app.models import (
    AdminHOD,
    Attendance,
    AttendanceReport,
    Courses,
    CustomUser,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    NotificationStaffs,
    NotificationStudent,
    SessionYearModel,
    Staffs,
    StudentResult,
    Students,
    Subjects,
)


class SessionYearModelTest(TestCase):
    """Test cases for SessionYearModel."""

    def setUp(self):
        """Set up test data."""
        self.session = SessionYearModel.objects.create(
            session_start_year=date(2024, 1, 1),
            session_end_year=date(2024, 12, 31),
        )

    def test_session_year_creation(self):
        """Test that a session year can be created."""
        self.assertIsNotNone(self.session.id)
        self.assertEqual(self.session.session_start_year, date(2024, 1, 1))
        self.assertEqual(self.session.session_end_year, date(2024, 12, 31))


class CustomUserTest(TestCase):
    """Test cases for CustomUser model."""

    def test_create_hod_user(self):
        """Test creating an HOD user."""
        user = CustomUser.objects.create_user(
            username="hod_test",
            email="hod@test.com",
            password="testpass123",
            user_type=1,
        )
        self.assertEqual(str(user.user_type), "1")
        self.assertTrue(user.check_password("testpass123"))

    def test_create_staff_user(self):
        """Test creating a Staff user."""
        user = CustomUser.objects.create_user(
            username="staff_test",
            email="staff@test.com",
            password="testpass123",
            user_type=2,
        )
        self.assertEqual(str(user.user_type), "2")

    def test_create_student_user(self):
        """Test creating a Student user."""
        SessionYearModel.objects.create(
            session_start_year=date(2024, 1, 1),
            session_end_year=date(2024, 12, 31),
        )
        Courses.objects.create(course_name="Test Course")
        user = CustomUser.objects.create_user(
            username="student_test",
            email="student@test.com",
            password="testpass123",
            user_type=3,
        )
        self.assertEqual(str(user.user_type), "3")


class CoursesTest(TestCase):
    """Test cases for Courses model."""

    def setUp(self):
        """Set up test data."""
        self.course = Courses.objects.create(course_name="Computer Science")

    def test_course_creation(self):
        """Test that a course can be created."""
        self.assertIsNotNone(self.course.id)
        self.assertEqual(self.course.course_name, "Computer Science")
        self.assertIsNotNone(self.course.created_at)
        self.assertIsNotNone(self.course.updated_at)


class SubjectsTest(TestCase):
    """Test cases for Subjects model."""

    def setUp(self):
        """Set up test data."""
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
        self.subject = Subjects.objects.create(
            subject_name="Python Programming",
            course_id=self.course,
            staff_id=self.staff_user,
        )

    def test_subject_creation(self):
        """Test that a subject can be created."""
        self.assertIsNotNone(self.subject.id)
        self.assertEqual(self.subject.subject_name, "Python Programming")
        self.assertEqual(self.subject.course_id, self.course)
        self.assertEqual(self.subject.staff_id, self.staff_user)


class AttendanceTest(TestCase):
    """Test cases for Attendance model."""

    def setUp(self):
        """Set up test data."""
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
        self.subject = Subjects.objects.create(
            subject_name="Python Programming",
            course_id=self.course,
            staff_id=self.staff_user,
        )
        self.attendance = Attendance.objects.create(
            subject_id=self.subject,
            attendance_date=date(2024, 6, 15),
            session_year_id=self.session,
        )

    def test_attendance_creation(self):
        """Test that attendance can be recorded."""
        self.assertIsNotNone(self.attendance.id)
        self.assertEqual(self.attendance.subject_id, self.subject)
        self.assertEqual(self.attendance.attendance_date, date(2024, 6, 15))


class LeaveReportTest(TestCase):
    """Test cases for Leave Report models."""

    def setUp(self):
        """Set up test data."""
        self.session = SessionYearModel.objects.create(
            session_start_year=date(2024, 1, 1),
            session_end_year=date(2024, 12, 31),
        )
        self.course = Courses.objects.create(course_name="Computer Science")

    def test_student_leave_report_creation(self):
        """Test creating a student leave report."""
        student_user = CustomUser.objects.create_user(
            username="student_test",
            email="student@test.com",
            password="testpass123",
            user_type=3,
        )
        student = Students.objects.get(admin=student_user)
        student.address = "Test Address"
        student.gender = "Male"
        student.save()

        leave_report = LeaveReportStudent.objects.create(
            student_id=student,
            leave_date="2024-06-15",
            leave_message="Sick leave",
            leave_status=0,
        )
        self.assertIsNotNone(leave_report.id)
        self.assertEqual(leave_report.leave_message, "Sick leave")
        self.assertEqual(leave_report.leave_status, 0)


class FeedbackTest(TestCase):
    """Test cases for Feedback models."""

    def setUp(self):
        """Set up test data."""
        self.session = SessionYearModel.objects.create(
            session_start_year=date(2024, 1, 1),
            session_end_year=date(2024, 12, 31),
        )
        self.course = Courses.objects.create(course_name="Computer Science")

    def test_student_feedback_creation(self):
        """Test creating student feedback."""
        student_user = CustomUser.objects.create_user(
            username="student_test",
            email="student@test.com",
            password="testpass123",
            user_type=3,
        )
        student = Students.objects.get(admin=student_user)
        student.address = "Test Address"
        student.gender = "Male"
        student.save()

        feedback = FeedBackStudent.objects.create(
            student_id=student,
            feedback="Great course!",
            feedback_reply="",
        )
        self.assertIsNotNone(feedback.id)
        self.assertEqual(feedback.feedback, "Great course!")


class StudentResultTest(TestCase):
    """Test cases for StudentResult model."""

    def setUp(self):
        """Set up test data."""
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
        self.subject = Subjects.objects.create(
            subject_name="Python Programming",
            course_id=self.course,
            staff_id=self.staff_user,
        )
        self.student_user = CustomUser.objects.create_user(
            username="student_test",
            email="student@test.com",
            password="testpass123",
            user_type=3,
        )
        self.student = Students.objects.get(admin=self.student_user)
        self.student.address = "Test Address"
        self.student.gender = "Male"
        self.student.save()

    def test_student_result_creation(self):
        """Test creating student result."""
        result = StudentResult.objects.create(
            student_id=self.student,
            subject_id=self.subject,
            subject_exam_marks=85.5,
            subject_assignment_marks=90.0,
        )
        self.assertIsNotNone(result.id)
        self.assertEqual(result.subject_exam_marks, 85.5)
        self.assertEqual(result.subject_assignment_marks, 90.0)
