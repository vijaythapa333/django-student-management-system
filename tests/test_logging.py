import os
import sys
import logging
import django
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')

django.setup()

from django.conf import settings
from django.test import TestCase, override_settings
import unittest


class LoggingFileCreationTestCase(TestCase):
    """测试日志文件创建"""

    def test_log_directory_exists(self):
        """测试日志目录是否存在"""
        self.assertTrue(os.path.exists(settings.LOG_DIR), 
                        f"日志目录 {settings.LOG_DIR} 不存在")

    def test_log_directory_is_writable(self):
        """测试日志目录是否可写"""
        test_file = os.path.join(settings.LOG_DIR, 'test_write.tmp')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            self.assertTrue(True)
        except IOError:
            self.fail(f"日志目录 {settings.LOG_DIR} 不可写")

    def test_debug_log_file_created_on_logging(self):
        """测试 debug.log 文件在记录日志时创建"""
        logger = logging.getLogger('student_management_app')
        logger.debug(f"测试 debug 日志 - {datetime.now()}")
        
        debug_log_path = os.path.join(settings.LOG_DIR, 'debug.log')
        self.assertTrue(os.path.exists(debug_log_path), 
                        f"debug.log 文件不存在于 {settings.LOG_DIR}")

    def test_error_log_file_created_on_logging(self):
        """测试 error.log 文件在记录错误日志时创建"""
        logger = logging.getLogger('student_management_app')
        logger.error(f"测试 error 日志 - {datetime.now()}")
        
        error_log_path = os.path.join(settings.LOG_DIR, 'error.log')
        self.assertTrue(os.path.exists(error_log_path), 
                        f"error.log 文件不存在于 {settings.LOG_DIR}")


class LoggingContentTestCase(TestCase):
    """测试日志内容格式"""

    def setUp(self):
        self.test_message = f"测试消息内容 {datetime.now().isoformat()}"
        self.logger = logging.getLogger('student_management_app.test')

    def test_log_contains_timestamp(self):
        """测试日志包含时间戳"""
        self.logger.info(self.test_message)
        
        debug_log_path = os.path.join(settings.LOG_DIR, 'debug.log')
        with open(debug_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(self.test_message, content)
        self.assertRegex(content, r'\d{4}-\d{2}-\d{2}')

    def test_log_contains_level(self):
        """测试日志包含级别信息"""
        self.logger.warning(self.test_message)
        
        debug_log_path = os.path.join(settings.LOG_DIR, 'debug.log')
        with open(debug_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('[WARNING]', content)
        self.assertIn(self.test_message, content)

    def test_log_contains_module_info(self):
        """测试日志包含模块信息"""
        self.logger.info(self.test_message)
        
        debug_log_path = os.path.join(settings.LOG_DIR, 'debug.log')
        with open(debug_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('test_logging', content)

    def test_log_contains_line_number(self):
        """测试日志包含行号"""
        self.logger.info(self.test_message)
        
        debug_log_path = os.path.join(settings.LOG_DIR, 'debug.log')
        with open(debug_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertRegex(content, r'\(\d+\):')

    def test_error_log_receives_errors_only(self):
        """测试 error.log 只接收错误级别日志"""
        test_error = f"测试错误消息 {datetime.now().isoformat()}"
        test_info = f"测试信息消息 {datetime.now().isoformat()}"
        
        logger = logging.getLogger('student_management_app.error_test')
        logger.info(test_info)
        logger.error(test_error)
        
        error_log_path = os.path.join(settings.LOG_DIR, 'error.log')
        with open(error_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(test_error, content)
        self.assertNotIn(test_info, content)


class LoggingHandlerTestCase(TestCase):
    """测试日志处理器配置"""

    def test_debug_handler_rotation_config(self):
        """测试 debug 日志处理器切割配置"""
        handler = settings.LOGGING['handlers']['debug_file']
        self.assertEqual(handler['when'], 'midnight')
        self.assertEqual(handler['backupCount'], 30)
        self.assertEqual(handler['encoding'], 'utf-8')

    def test_error_handler_rotation_config(self):
        """测试 error 日志处理器切割配置"""
        handler = settings.LOGGING['handlers']['error_file']
        self.assertEqual(handler['when'], 'midnight')
        self.assertEqual(handler['backupCount'], 30)
        self.assertEqual(handler['encoding'], 'utf-8')

    def test_access_handler_rotation_config(self):
        """测试 access 日志处理器切割配置"""
        handler = settings.LOGGING['handlers']['access_file']
        self.assertEqual(handler['when'], 'midnight')
        self.assertEqual(handler['backupCount'], 30)
        self.assertEqual(handler['encoding'], 'utf-8')


class LoggingFormatterTestCase(TestCase):
    """测试日志格式化器"""

    def test_verbose_formatter_format(self):
        """测试 verbose 格式化器格式"""
        formatter = settings.LOGGING['formatters']['verbose']
        self.assertIn('{asctime}', formatter['format'])
        self.assertIn('{levelname}', formatter['format'])
        self.assertIn('{module}', formatter['format'])
        self.assertIn('{lineno}', formatter['format'])
        self.assertIn('{message}', formatter['format'])

    def test_access_formatter_format(self):
        """测试 access 格式化器格式"""
        formatter = settings.LOGGING['formatters']['access']
        self.assertIn('{asctime}', formatter['format'])
        self.assertIn('{levelname}', formatter['format'])
        self.assertIn('{module}', formatter['format'])
        self.assertIn('{message}', formatter['format'])


class LoggingLevelTestCase(TestCase):
    """测试日志级别配置"""

    def test_django_logger_level(self):
        """测试 django 日志记录器级别"""
        logger_config = settings.LOGGING['loggers']['django']
        self.assertIn(logger_config['level'], ['DEBUG', 'INFO', 'WARNING', 'ERROR'])

    def test_app_logger_level(self):
        """测试应用日志记录器级别"""
        logger_config = settings.LOGGING['loggers']['student_management_app']
        self.assertIn(logger_config['level'], ['DEBUG', 'INFO', 'WARNING', 'ERROR'])

    def test_django_request_logger_receives_errors(self):
        """测试 django.request 日志记录器接收错误"""
        logger_config = settings.LOGGING['loggers']['django.request']
        self.assertEqual(logger_config['level'], 'ERROR')
        self.assertIn('error_file', logger_config['handlers'])


class LoggingIntegrationTestCase(TestCase):
    """日志系统集成测试"""

    def test_logger_hierarchy(self):
        """测试日志记录器层级"""
        logger = logging.getLogger('student_management_app')
        self.assertIsNotNone(logger)
        
        child_logger = logging.getLogger('student_management_app.views')
        self.assertEqual(child_logger.parent, logger)

    def test_multiple_log_levels_to_same_file(self):
        """测试多个日志级别写入同一文件"""
        logger = logging.getLogger('student_management_app.multi_level')
        
        test_messages = {
            'DEBUG': f"DEBUG 消息 {datetime.now().isoformat()}",
            'INFO': f"INFO 消息 {datetime.now().isoformat()}",
            'WARNING': f"WARNING 消息 {datetime.now().isoformat()}",
        }
        
        logger.debug(test_messages['DEBUG'])
        logger.info(test_messages['INFO'])
        logger.warning(test_messages['WARNING'])
        
        debug_log_path = os.path.join(settings.LOG_DIR, 'debug.log')
        with open(debug_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for level, msg in test_messages.items():
            self.assertIn(msg, content, f"{level} 消息未写入 debug.log")

    def test_console_handler_exists(self):
        """测试控制台处理器存在"""
        handler = settings.LOGGING['handlers']['console']
        self.assertEqual(handler['class'], 'logging.StreamHandler')
        self.assertEqual(handler['formatter'], 'verbose')


class LoggingRotationSimulationTestCase(TestCase):
    """模拟日志切割测试"""

    def test_handler_supports_rotation(self):
        """测试处理器支持切割"""
        from logging.handlers import TimedRotatingFileHandler
        
        for handler_name in ['debug_file', 'error_file', 'access_file']:
            handler_config = settings.LOGGING['handlers'][handler_name]
            handler_class = handler_config['class']
            self.assertEqual(handler_class, 'logging.handlers.TimedRotatingFileHandler',
                           f"{handler_name} 不是 TimedRotatingFileHandler")

    def test_backup_count_is_30(self):
        """测试备份文件数量为 30"""
        for handler_name in ['debug_file', 'error_file', 'access_file']:
            handler = settings.LOGGING['handlers'][handler_name]
            self.assertEqual(handler['backupCount'], 30,
                           f"{handler_name} 的 backupCount 不是 30")

    def test_rotation_interval_is_daily(self):
        """测试切割间隔为每天"""
        for handler_name in ['debug_file', 'error_file', 'access_file']:
            handler = settings.LOGGING['handlers'][handler_name]
            self.assertEqual(handler['when'], 'midnight',
                           f"{handler_name} 的 when 不是 midnight")


if __name__ == '__main__':
    unittest.main()
