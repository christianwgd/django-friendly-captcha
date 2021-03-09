from django.conf import settings
from django.forms import Widget
from django.template import loader
from django.utils import translation
from django.utils.safestring import mark_safe


class FrcCaptchaWidget(Widget):
    template_name = 'friendly_captcha/frc_captcha_widget.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context['locale'] = translation.get_language()
        context['captcha_sitekey'] = getattr(settings, 'FRC_CAPTCHA_SITE_KEY', None)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)