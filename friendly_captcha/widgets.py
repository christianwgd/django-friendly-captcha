from django.conf import settings
from django.forms import Widget
from django.forms.utils import flatatt
from django.utils import translation
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from friendly_captcha.utils import (
    get_captcha_endpoint,
    get_captcha_version,
    get_start_mode,
    get_widget_field_name_attr,
    get_widget_language_attr,
    get_widget_script_urls,
)


class FrcCaptchaWidget(Widget):

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.site_key = getattr(settings, 'FRC_CAPTCHA_SITE_KEY', None)
        self.frc_widget_module_js, self.frc_widget_js = get_widget_script_urls()

    def render(self, name, value, attrs=None, renderer=None):
        if self.site_key is not None:
            self.attrs['data-sitekey'] = self.site_key
        self.attrs.setdefault('data-start', get_start_mode())
        self.attrs[get_widget_language_attr()] = translation.get_language()
        if get_captcha_version() == 2:
            self.attrs['data-api-endpoint'] = get_captcha_endpoint()
        else:
            self.attrs['data-puzzle-endpoint'] = get_captcha_endpoint()
        self.attrs[get_widget_field_name_attr()] = name
        self.attrs['class'] = 'frc-captcha'
        final_attrs = self.build_attrs(self.attrs)
        frc_widget_module_js, self.frc_widget_js = get_widget_script_urls()
        frc_js = mark_safe(
            f'<script type="module" src="{frc_widget_module_js}" async defer></script>'
            f'<script nomodule src="{self.frc_widget_js}" async defer></script>',
        )
        return format_html('<div {}></div>{}', flatatt(final_attrs), frc_js)
