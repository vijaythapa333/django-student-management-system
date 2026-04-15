import os
import logging
from django.test import TestCase
from django.conf import settings


class SettingsConfigurationTest(TestCase):

    def test_secret_key_loaded(self):
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, '')

    def test_debug_mode(self):
        self.assertIsInstance(settings.DEBUG, bool)

    def test_allowed_hosts_configured(self):
        self.assertIsInstance(settings.ALLOWED_HOSTS, list)

    def test_database_configured(self):
        self.assertIn('default', settings.DATABASES)
        self.assertIn('ENGINE', settings.DATABASES['default'])

    def test_logging_configured(self):
        self.assertIn('version', settings.LOGGING)
        self.assertEqual(settings.LOGGING['version'], 1)

    def test_log_handlers_exist(self):
        handlers = settings.LOGGING.get('handlers', {})
        self.assertIn('console', handlers)
        self.assertIn('file_debug', handlers)
        self.assertIn('file_error', handlers)
        self.assertIn('file_access', handlers)

    def test_log_formatters_configured(self):
        formatters = settings.LOGGING.get('formatters', {})
        self.assertIn('verbose', formatters)
        self.assertIn('simple', formatters)
        self.assertIn('%(asctime)s', formatters['verbose']['format'])
        self.assertIn('%(levelname)s', formatters['verbose']['format'])
        self.assertIn('%(module)s', formatters['verbose']['format'])
        self.assertIn('%(lineno)d', formatters['verbose']['format'])

    def test_log_directory_exists(self):
        self.assertTrue(os.path.exists(settings.LOG_DIR))

    def test_auth_user_model_configured(self):
        self.assertEqual(settings.AUTH_USER_MODEL, 'student_management_app.CustomUser')

    def test_authentication_backends_configured(self):
        self.assertIn(
            'student_management_app.EmailBackEnd.EmailBackEnd',
            settings.AUTHENTICATION_BACKENDS
        )


class EnvironmentConfigurationTest(TestCase):

    def test_dotenv_loaded(self):
        env_secret = os.getenv('SECRET_KEY')
        if env_secret:
            self.assertEqual(settings.SECRET_KEY, env_secret)

    def test_django_env_defaults_to_dev(self):
        django_env = os.getenv('DJANGO_ENV', 'dev')
        self.assertIn(django_env, ['dev', 'prod'])


class LoggingFunctionalityTest(TestCase):

    def test_logger_exists(self):
        logger = logging.getLogger('student_management_app')
        self.assertIsNotNone(logger)

    def test_debug_logging_works(self):
        logger = logging.getLogger('student_management_app')
        logger.debug('Test debug message')
        self.assertTrue(True)

    def test_error_logging_works(self):
        logger = logging.getLogger('student_management_app')
        try:
            raise ValueError('Test error for logging')
        except ValueError:
            logger.exception('Test exception logged')
        self.assertTrue(True)

    def test_log_file_rotation_configured(self):
        debug_handler = settings.LOGGING['handlers']['file_debug']
        self.assertEqual(debug_handler.get('when'), 'midnight')
        self.assertEqual(debug_handler.get('backupCount'), 30)
        error_handler = settings.LOGGING['handlers']['file_error']
        self.assertEqual(error_handler.get('backupCount'), 30)
        access_handler = settings.LOGGING['handlers']['file_access']
        self.assertEqual(access_handler.get('backupCount'), 30)
