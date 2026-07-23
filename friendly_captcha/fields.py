from logging import getLogger

import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from friendly_captcha.utils import (
    get_captcha_version,
    get_verification_payload,
    get_verification_url,
)
from friendly_captcha.widgets import FrcCaptchaWidget

logger = getLogger('django.friendly_captcha')


class FrcCaptchaField(forms.CharField):
    description = "Friendly captcha field"
    widget = FrcCaptchaWidget

    def __init__(self, *args, **kwargs):
        super(FrcCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # Mock the response of verification for testing purposes
        mocked_value = getattr(settings, 'FRC_CAPTCHA_MOCKED_VALUE', None)
        if mocked_value is not None:
            logger.info('Captcha mocked value set to %s', mocked_value)
            return mocked_value

        clean_value = False
        captcha_sitekey = getattr(settings, 'FRC_CAPTCHA_SITE_KEY', None)
        captcha_verification_url = get_verification_url()
        captcha_version = get_captcha_version()
        captcha_api_key = getattr(settings, 'FRC_CAPTCHA_API_KEY', None)
       
        captcha_ready = bool(captcha_sitekey and captcha_api_key and captcha_verification_url)

        if captcha_ready:
            payload = get_verification_payload(value)
            payload['sitekey'] = captcha_sitekey
            if captcha_version == 2:
                headers = {'X-API-Key': captcha_api_key}
            else:
                payload['secret'] = captcha_api_key
                headers = {}

            captcha_response = requests.post(
                captcha_verification_url,
                data=payload,
                headers=headers,
                timeout=20,
            )
            if captcha_response.status_code == 200:
                validation = captcha_response.json()
                if not validation.get('success'):
                    logger.info('Captcha failed validation %s', validation)
                else:
                    logger.info('Captcha validation success')
                    clean_value = True                

            else:  # Unverified response
                logger.info('Captcha failed validation (code %s) %s', captcha_response.status_code, captcha_response.text)
                accept_unverified = getattr(settings, 'FRC_CAPTCHA_ACCEPT_UNVERIFIED', False)
                if accept_unverified:
                    logger.info(
                        'Captcha could not be verified, accepting unverified response (code %s) %s',
                        captcha_response.status_code, captcha_response.text
                    )
                    clean_value = True

        if clean_value:
            return True
        fail_silent = getattr(settings, 'FRC_CAPTCHA_FAIL_SILENT', False)
        if fail_silent:
            return False
        raise ValidationError(_('Captcha test failed'), code='bot_detected')
