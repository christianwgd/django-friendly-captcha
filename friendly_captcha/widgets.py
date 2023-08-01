from django.conf import settings
from django.forms import Widget
from django.utils import translation
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class FrcCaptchaWidget(Widget):

    def __init__(self):
        super().__init__()
        self.site_key = getattr(settings, 'FRC_CAPTCHA_SITE_KEY', None)
        self.frc_widget_module_js = getattr(
            settings, 'FRC_WIDGET_MODULE_JS',
            'https://unpkg.com/friendly-challenge@0.9.12/widget.module.min.js',
        )
        self.frc_widget_js = getattr(
            settings, 'FRC_WIDGET_JS',
            'https://unpkg.com/friendly-challenge@0.9.12/widget.min.js'
        )

    def render(self, name, value, attrs=None, renderer=None):
        attrs['data-lang'] = translation.get_language()
        attrs['data-sitekey'] = self.site_key
        attrs['data-solution-field-name'] = name
        attrs['class'] = 'frc-captcha'
        final_attrs = self.build_attrs(attrs)
        frc_js = mark_safe(
            f'<script type="module" src="{self.frc_widget_module_js}" async defer></script>'
            f'<script nomodule src="{self.frc_widget_js}" async defer></script>'
        )
        return format_html('<div {}></div>{}', flatatt(final_attrs), frc_js)
