"""Exercise both notification paths with synthetic config and mocked SMTP."""

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import smtplib
import ssl
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, mock_open, patch


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC = {
    "SMTP_USERNAME": "sender@example.invalid",
    "SMTP_PASSWORD": "synthetic-smtp-test-only",
    "SMTP_RECIPIENT": "recipient@example.invalid",
}


class SMTPConfigTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ, {}, clear=True))
        self.stack.enter_context(patch("socket.create_connection", side_effect=AssertionError("No network")))
        self.output = io.StringIO()
        self.stack.enter_context(contextlib.redirect_stdout(self.output))
        self.lxml = ModuleType("lxml")
        self.lxml.etree = Mock()
        self.scrapy = ModuleType("scrapy")
        self.mail = ModuleType("scrapy.mail")
        self.mail.MailSender = Mock()
        self.stack.enter_context(patch.dict(sys.modules, {
            "lxml": self.lxml, "scrapy": self.scrapy, "scrapy.mail": self.mail,
        }))
        self.smtp = self.stack.enter_context(patch.object(smtplib, "SMTP_SSL"))
        self.standalone = self.load("NovelSpider/update/Update.py", "standalone_test")
        self.pipeline = self.load("NovelSpider/updateScrapy/update/pipelines.py", "pipeline_test")

    def load(self, file, name):
        spec = importlib.util.spec_from_file_location(name, ROOT / file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_pipeline(self):
        item = {"chapter": "synthetic-new-chapter", "update_time": "synthetic-time"}
        with patch("builtins.open", mock_open(read_data="old\ttime\n")) as opened:
            result = self.pipeline.NovelPipeline().process_item(item, None)
        self.assertIs(result, item)
        return opened

    def test_import_never_connects(self):
        self.smtp.assert_not_called()
        self.mail.MailSender.assert_not_called()

    def test_standalone_requires_each_setting_before_connecting(self):
        for name in SYNTHETIC:
            with self.subTest(name=name), patch.dict(os.environ, SYNTHETIC, clear=True):
                del os.environ[name]
                with self.assertRaisesRegex(ValueError, name):
                    self.standalone.SendEmail("synthetic-title").send("https://example.invalid/chapter")
        self.smtp.assert_not_called()

    def test_standalone_uses_env_tls_timeout_and_no_debug(self):
        os.environ.update(SYNTHETIC)
        self.standalone.SendEmail("synthetic-title").send("https://example.invalid/chapter")
        args, kwargs = self.smtp.call_args
        self.assertEqual(args, ("smtp.163.com", 465))
        self.assertEqual(kwargs["timeout"], 30)
        self.assertIsInstance(kwargs["context"], ssl.SSLContext)
        self.assertEqual(kwargs["context"].verify_mode, ssl.CERT_REQUIRED)
        server = self.smtp.return_value.__enter__.return_value
        server.login.assert_called_once_with(SYNTHETIC["SMTP_USERNAME"], SYNTHETIC["SMTP_PASSWORD"])
        server.set_debuglevel.assert_not_called()
        self.assertNotIn(SYNTHETIC["SMTP_PASSWORD"], self.output.getvalue())

    def test_standalone_hides_authentication_exception(self):
        os.environ.update(SYNTHETIC)
        server = self.smtp.return_value.__enter__.return_value
        server.login.side_effect = smtplib.SMTPException(SYNTHETIC["SMTP_PASSWORD"])
        self.standalone.SendEmail("synthetic-title").send("https://example.invalid/chapter")
        server.sendmail.assert_not_called()
        self.assertNotIn(SYNTHETIC["SMTP_PASSWORD"], self.output.getvalue())
        self.assertIn("details withheld", self.output.getvalue())

    def test_pipeline_requires_each_setting_before_sender_creation(self):
        for name in SYNTHETIC:
            with self.subTest(name=name), patch.dict(os.environ, SYNTHETIC, clear=True):
                del os.environ[name]
                with self.assertRaisesRegex(ValueError, name):
                    self.run_pipeline()
        self.mail.MailSender.assert_not_called()

    def test_pipeline_uses_env_and_ssl_without_debug(self):
        os.environ.update(SYNTHETIC)
        self.run_pipeline()
        kwargs = self.mail.MailSender.call_args.kwargs
        self.assertEqual(kwargs["smtpuser"], SYNTHETIC["SMTP_USERNAME"])
        self.assertEqual(kwargs["smtppass"], SYNTHETIC["SMTP_PASSWORD"])
        self.assertEqual(kwargs["smtpport"], 465)
        self.assertTrue(kwargs["smtpssl"])
        self.assertFalse(kwargs["debug"])
        self.assertEqual(self.mail.MailSender.return_value.send.call_args.kwargs["to"], [SYNTHETIC["SMTP_RECIPIENT"]])

    def test_custom_host_port_and_sender(self):
        os.environ.update(SYNTHETIC, SMTP_HOST="smtp.example.invalid", SMTP_PORT="2465", SMTP_FROM="notice@example.invalid")
        self.run_pipeline()
        kwargs = self.mail.MailSender.call_args.kwargs
        self.assertEqual(kwargs["smtphost"], "smtp.example.invalid")
        self.assertEqual(kwargs["smtpport"], 2465)
        self.assertEqual(kwargs["mailfrom"], "notice@example.invalid")


if __name__ == "__main__":
    unittest.main()
