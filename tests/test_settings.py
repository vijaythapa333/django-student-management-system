import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')

django.setup()

from django.conf import settings
from django.test import TestCase
import unittest


class SettingsBaseTestCase(TestCase):
    """测试基础配置"""

    def test_base_dir_exists(self):
        """测试 BASE_DIR 是否正确设置"""
        self.assertTrue(hasattr(settings, 'BASE_DIR'))
        self.assertTrue(settings.BASE_DIR.exists())

    def test_secret_key_not_empty(self):
        """测试 SECRET_KEY 不为空"""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, '')

    def test_installed_apps_contains_required_apps(self):
        """测试必需的应用是否已安装"""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'student_management_app',
        ]
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_middleware_configured(self):
        """测试中间件是否正确配置"""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        for middleware in required_middleware:
            self.assertIn(middleware, settings.MIDDLEWARE)

    def test_custom_user_model(self):
        """测试自定义用户模型配置"""
        self.assertEqual(settings.AUTH_USER_MODEL, "student_management_app.CustomUser")

    def test_authentication_backends(self):
        """测试自定义认证后端"""
        self.assertIn('student_management_app.EmailBackEnd.EmailBackEnd', 
                      settings.AUTHENTICATION_BACKENDS)


class SettingsLoggingTestCase(TestCase):
    """测试日志配置"""

    def test_logging_configured(self):
        """测试日志系统是否配置"""
        self.assertTrue(hasattr(settings, 'LOGGING'))
        self.assertIn('version', settings.LOGGING)
        self.assertEqual(settings.LOGGING['version'], 1)

    def test_logging_formatters_exist(self):
        """测试日志格式化器是否存在"""
        formatters = settings.LOGGING.get('formatters', {})
        self.assertIn('verbose', formatters)
        self.assertIn('simple', formatters)
        self.assertIn('access', formatters)

    def test_logging_handlers_exist(self):
        """测试日志处理器是否存在"""
        handlers = settings.LOGGING.get('handlers', {})
        self.assertIn('console', handlers)
        self.assertIn('debug_file', handlers)
        self.assertIn('error_file', handlers)
        self.assertIn('access_file', handlers)

    def test_logging_handlers_rotation(self):
        """测试日志处理器是否配置了按天切割"""
        for handler_name in ['debug_file', 'error_file', 'access_file']:
            handler = settings.LOGGING['handlers'][handler_name]
            self.assertEqual(handler['when'], 'midnight')
            self.assertEqual(handler['backupCount'], 30)

    def test_loggers_configured(self):
        """测试日志记录器是否配置"""
        loggers = settings.LOGGING.get('loggers', {})
        self.assertIn('django', loggers)
        self.assertIn('django.request', loggers)
        self.assertIn('django.server', loggers)
        self.assertIn('student_management_app', loggers)

    def test_log_dir_exists(self):
        """测试日志目录配置"""
        self.assertTrue(hasattr(settings, 'LOG_DIR'))
        self.assertTrue(os.path.exists(settings.LOG_DIR))


class SettingsDatabaseTestCase(TestCase):
    """测试数据库配置"""

    def test_database_configured(self):
        """测试数据库是否配置"""
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
        self.assertIn('ENGINE', settings.DATABASES['default'])

    def test_database_engine(self):
        """测试数据库引擎"""
        engine = settings.DATABASES['default']['ENGINE']
        self.assertIn(engine, [
            'django.db.backends.sqlite3',
            'django.db.backends.mysql',
            'django.db.backends.postgresql',
        ])


class SettingsStaticMediaTestCase(TestCase):
    """测试静态文件和媒体文件配置"""

    def test_static_url_configured(self):
        """测试静态文件 URL 配置"""
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(settings.STATIC_URL.startswith('/'))

    def test_media_url_configured(self):
        """测试媒体文件 URL 配置"""
        self.assertTrue(hasattr(settings, 'MEDIA_URL'))
        self.assertTrue(settings.MEDIA_URL.startswith('/'))

    def test_media_root_configured(self):
        """测试媒体文件根目录配置"""
        self.assertTrue(hasattr(settings, 'MEDIA_ROOT'))


class EnvironmentVariablesTestCase(TestCase):
    """测试环境变量配置"""

    def test_dotenv_loaded(self):
        """测试 .env 文件是否被加载"""
        from dotenv import load_dotenv
        load_dotenv()
        self.assertIsNotNone(os.environ.get('DJANGO_ENV', None))

    def test_env_file_exists(self):
        """测试 .env 文件是否存在"""
        env_example_path = BASE_DIR / '.env.example'
        self.assertTrue(env_example_path.exists())


class SettingsModuleImportTestCase(TestCase):
    """测试配置模块导入"""

    def test_import_base_settings(self):
        """测试导入 base 配置"""
        import student_management_system.settings.base as base_settings
        self.assertTrue(hasattr(base_settings, 'BASE_DIR'))

    def test_import_dev_settings(self):
        """测试导入 dev 配置"""
        import student_management_system.settings.dev as dev_settings
        self.assertTrue(hasattr(dev_settings, 'DEBUG'))

    def test_import_prod_settings(self):
        """测试导入 prod 配置"""
        import student_management_system.settings.prod as prod_settings
        self.assertTrue(hasattr(prod_settings, 'DEBUG'))


if __name__ == '__main__':
    unittest.main()
