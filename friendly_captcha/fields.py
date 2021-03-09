from logging import getLogger

import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from friendly_captcha.widgets import FrcCaptchaWidget

logger = getLogger('django.friendly_captcha')


class FrcCaptchaField(forms.CharField):
    description = "Friendly captcha field"
    widget = FrcCaptchaWidget

    def __init__(self, *args, **kwargs):
        super(FrcCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, value):
        clean_value = False
        # handle captcha field
        captcha_secret = getattr(settings, 'FRC_CAPTCHA_SECRET', None)
        captcha_sitekey = getattr(settings, 'FRC_CAPTCHA_SITE_KEY', None)
        captcha_verification_url = getattr(settings, 'FRC_CAPTCHA_VERIFICATION_URL', False)
        if captcha_sitekey and captcha_secret and captcha_verification_url:
            payload = {
                'solution': value,
                'secret': captcha_secret,
                'sitekey': captcha_sitekey
            }
            captcha_response = requests.post(captcha_verification_url, data=payload)
            if captcha_response.status_code == 200:
                validation = captcha_response.json()
                if not validation['success']:
                    logger.info('Captcha failed validation {}'.format(captcha_response.json()))
                else:
                    logger.info('Captcha validation success')
                    clean_value = True
            else:
                logger.info('Captcha failed validation {}'.format(captcha_response.json()))

        if clean_value:
            return True
        else:
            fail_silent = getattr(settings, 'FRC_CAPTCHA_FAIL_SILENT', False)
            if fail_silent:
                return False
            else:
                raise ValidationError(_('Captcha test failed'), code='bot_detected')
