from django.conf import settings
from django.forms import Widget
from django.utils import translation
from django.utils.html import format_html
from django.forms.utils import flatatt


class FrcCaptchaWidget(Widget):

    def render(self, name, value, attrs=None, renderer=None):
        attrs['data-lang'] = translation.get_language()
        attrs['data-sitekey'] = getattr(settings, 'FRC_CAPTCHA_SITE_KEY', None)
        attrs['class'] = 'frc-captcha'
        final_attrs = self.build_attrs(attrs)
        return format_html('<div {}></div>', flatatt(final_attrs))
