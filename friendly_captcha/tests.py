import django
import pytest
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock
from friendly_captcha.fields import FrcCaptchaField
from friendly_captcha.widgets import FrcCaptchaWidget
from django.conf import settings


settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'friendly_captcha',
    ],
)
django.setup()


class FrcCaptchaWidgetTest(TestCase):
    @override_settings(FRC_CAPTCHA_SITE_KEY='test-site-key')
    def test_render(self):
        widget = FrcCaptchaWidget()
        html = widget.render('captcha-field', None, attrs={})
        self.assertIn('class="frc-captcha"', html)
        self.assertIn('data-sitekey="test-site-key"', html)
        self.assertIn('data-solution-field-name="captcha-field"', html)
        self.assertIn('<script type="module"', html)
        self.assertIn('<script nomodule', html)

    @override_settings(FRC_CAPTCHA_SITE_KEY='test-site-key')
    def test_render_no_attrs(self):
        widget = FrcCaptchaWidget()
        # This should not raise TypeError
        html = widget.render('captcha-field', None)
        self.assertIn('class="frc-captcha"', html)
        self.assertIn('data-sitekey="test-site-key"', html)
        self.assertIn('data-solution-field-name="captcha-field"', html)
        self.assertIn('<script type="module"', html)
        self.assertIn('<script nomodule', html)

class FrcCaptchaFieldTest(TestCase):
    def test_clean_fails_without_settings(self):
        field = FrcCaptchaField()
        with pytest.raises(ValidationError):
            field.clean('some-value')

    @override_settings(FRC_CAPTCHA_FAIL_SILENT=True)
    def test_clean_fails_silently(self):
        field = FrcCaptchaField()
        result = field.clean('some-value')
        self.assertFalse(result)

    @override_settings(FRC_CAPTCHA_MOCKED_VALUE=True)
    def test_clean_mocked_value(self):
        field = FrcCaptchaField()
        result = field.clean('some-value')
        self.assertTrue(result)

    @patch('friendly_captcha.fields.requests.post')
    @override_settings(
        FRC_CAPTCHA_SECRET='test-secret',  # noqa: S106 Possible hardcoded password
        FRC_CAPTCHA_SITE_KEY='test-site-key',
        FRC_CAPTCHA_VERIFICATION_URL='http://test-url.com'
    )
    def test_clean_verification_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response

        field = FrcCaptchaField()
        result = field.clean('some-value')
        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch('friendly_captcha.fields.requests.post')
    @override_settings(
        FRC_CAPTCHA_SECRET='test-secret',  # noqa: S106 Possible hardcoded password
        FRC_CAPTCHA_SITE_KEY='test-site-key',
        FRC_CAPTCHA_VERIFICATION_URL='http://test-url.com'
    )
    def test_clean_verification_fail(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': False}
        mock_post.return_value = mock_response

        field = FrcCaptchaField()
        with pytest.raises(ValidationError):
            field.clean('some-value')

    @patch('friendly_captcha.fields.requests.post')
    @override_settings(
        FRC_CAPTCHA_SECRET='test-secret',  # noqa: S106 Possible hardcoded password
        FRC_CAPTCHA_SITE_KEY='test-site-key',
        FRC_CAPTCHA_VERIFICATION_URL='http://test-url.com'
    )
    def test_clean_verification_fail_not_200(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'success': False}
        mock_post.return_value = mock_response

        field = FrcCaptchaField()
        with pytest.raises(ValidationError):
            field.clean('some-value')
