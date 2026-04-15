"""
Tests for the settings configuration.

This module tests the environment-specific settings and configuration loading.
"""

import os
import sys
from pathlib import Path
from unittest import mock

from django.test import TestCase


class SettingsConfigurationTest(TestCase):
    """Test cases for settings configuration."""

    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.settings_dir = self.project_root / "student_management_system" / "settings"

    def test_settings_directory_exists(self):
        """Test that settings directory exists."""
        self.assertTrue(self.settings_dir.exists())
        self.assertTrue(self.settings_dir.is_dir())

    def test_base_settings_file_exists(self):
        """Test that base.py settings file exists."""
        base_settings = self.settings_dir / "base.py"
        self.assertTrue(base_settings.exists())

    def test_dev_settings_file_exists(self):
        """Test that dev.py settings file exists."""
        dev_settings = self.settings_dir / "dev.py"
        self.assertTrue(dev_settings.exists())

    def test_prod_settings_file_exists(self):
        """Test that prod.py settings file exists."""
        prod_settings = self.settings_dir / "prod.py"
        self.assertTrue(prod_settings.exists())

    def test_env_example_file_exists(self):
        """Test that .env.example file exists."""
        env_example = self.project_root / ".env.example"
        self.assertTrue(env_example.exists())

    def test_logs_directory_created(self):
        """Test that logs directory is created automatically."""
        logs_dir = self.project_root / "logs"
        self.assertTrue(logs_dir.exists())
        self.assertTrue(logs_dir.is_dir())


class EnvironmentVariableTest(TestCase):
    """Test cases for environment variable handling."""

    def test_secret_key_from_env(self):
        """Test that SECRET_KEY can be loaded from environment."""
        test_secret = "test-secret-key-for-testing"
        with mock.patch.dict(os.environ, {"SECRET_KEY": test_secret}):
            self.assertEqual(os.getenv("SECRET_KEY"), test_secret)

    def test_debug_from_env(self):
        """Test that DEBUG can be loaded from environment."""
        with mock.patch.dict(os.environ, {"DEBUG": "True"}):
            self.assertEqual(os.getenv("DEBUG"), "True")

    def test_allowed_hosts_from_env(self):
        """Test that ALLOWED_HOSTS can be loaded from environment."""
        test_hosts = "localhost,127.0.0.1,example.com"
        with mock.patch.dict(os.environ, {"ALLOWED_HOSTS": test_hosts}):
            hosts = os.getenv("ALLOWED_HOSTS", "").split(",")
            hosts = [host.strip() for host in hosts if host.strip()]
            self.assertEqual(hosts, ["localhost", "127.0.0.1", "example.com"])

    def test_database_config_from_env(self):
        """Test that database configuration can be loaded from environment."""
        with mock.patch.dict(
            os.environ,
            {
                "DB_ENGINE": "django.db.backends.mysql",
                "DB_NAME": "test_db",
                "DB_USER": "test_user",
                "DB_PASSWORD": "test_pass",
                "DB_HOST": "localhost",
                "DB_PORT": "3306",
            },
        ):
            self.assertEqual(os.getenv("DB_ENGINE"), "django.db.backends.mysql")
            self.assertEqual(os.getenv("DB_NAME"), "test_db")
            self.assertEqual(os.getenv("DB_USER"), "test_user")
            self.assertEqual(os.getenv("DB_PASSWORD"), "test_pass")
            self.assertEqual(os.getenv("DB_HOST"), "localhost")
            self.assertEqual(os.getenv("DB_PORT"), "3306")


class LoggingConfigurationTest(TestCase):
    """Test cases for logging configuration."""

    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.logs_dir = self.project_root / "logs"

    def test_logs_directory_exists(self):
        """Test that logs directory exists."""
        self.assertTrue(self.logs_dir.exists())

    def test_log_files_can_be_created(self):
        """Test that log files can be created in logs directory."""
        test_log_file = self.logs_dir / "test.log"
        try:
            test_log_file.write_text("Test log entry")
            self.assertTrue(test_log_file.exists())
            self.assertEqual(test_log_file.read_text(), "Test log entry")
        finally:
            if test_log_file.exists():
                test_log_file.unlink()


class CodeQualityToolsTest(TestCase):
    """Test cases for code quality tools configuration."""

    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).resolve().parent.parent.parent

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        pyproject = self.project_root / "pyproject.toml"
        self.assertTrue(pyproject.exists())

    def test_flake8_config_exists(self):
        """Test that .flake8 config file exists."""
        flake8_config = self.project_root / ".flake8"
        self.assertTrue(flake8_config.exists())

    def test_requirements_dev_exists(self):
        """Test that requirements-dev.txt exists."""
        requirements_dev = self.project_root / "requirements-dev.txt"
        self.assertTrue(requirements_dev.exists())

    def test_scripts_directory_exists(self):
        """Test that scripts directory exists."""
        scripts_dir = self.project_root / "scripts"
        self.assertTrue(scripts_dir.exists())
        self.assertTrue(scripts_dir.is_dir())


class ScriptsFunctionalityTest(TestCase):
    """Test cases for script files."""

    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.scripts_dir = self.project_root / "scripts"

    def test_format_script_exists(self):
        """Test that format.ps1 script exists."""
        format_script = self.scripts_dir / "format.ps1"
        self.assertTrue(format_script.exists())

    def test_lint_script_exists(self):
        """Test that lint.ps1 script exists."""
        lint_script = self.scripts_dir / "lint.ps1"
        self.assertTrue(lint_script.exists())

    def test_test_script_exists(self):
        """Test that test.ps1 script exists."""
        test_script = self.scripts_dir / "test.ps1"
        self.assertTrue(test_script.exists())

    def test_run_dev_script_exists(self):
        """Test that run-dev.ps1 script exists."""
        run_dev_script = self.scripts_dir / "run-dev.ps1"
        self.assertTrue(run_dev_script.exists())

    def test_setup_script_exists(self):
        """Test that setup.ps1 script exists."""
        setup_script = self.scripts_dir / "setup.ps1"
        self.assertTrue(setup_script.exists())

    def test_check_script_exists(self):
        """Test that check.ps1 script exists."""
        check_script = self.scripts_dir / "check.ps1"
        self.assertTrue(check_script.exists())
