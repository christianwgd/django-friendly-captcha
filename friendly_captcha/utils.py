from django.conf import settings

V1_VERIFICATION_URL = 'https://api.friendlycaptcha.com/api/v1/siteverify'
V2_VERIFICATION_URL = 'https://global.frcapi.com/api/v2/captcha/siteverify'

V1_WIDGET_MODULE_JS = 'https://cdn.jsdelivr.net/npm/friendly-challenge@0.9.20/widget.module.min.js'
V1_WIDGET_JS = 'https://cdn.jsdelivr.net/npm/friendly-challenge@0.9.20/widget.min.js'

V2_WIDGET_MODULE_JS = 'https://cdn.jsdelivr.net/npm/@friendlycaptcha/sdk/site.min.js'
V2_WIDGET_JS = 'https://cdn.jsdelivr.net/npm/@friendlycaptcha/sdk/site.compat.min.js'


def get_captcha_version():
    configured_version = getattr(settings, 'FRC_CAPTCHA_VERSION', None)
    if configured_version in (1, '1'):
        return 1
    if configured_version in (2, '2'):
        return 2

    verification_url = getattr(settings, 'FRC_CAPTCHA_VERIFICATION_URL', None)
    if verification_url and '/api/v2/' in verification_url:
        return 2

    if getattr(settings, 'FRC_CAPTCHA_API_KEY', None):
        return 2

    return 1


def get_verification_url():
    configured_url = getattr(settings, 'FRC_CAPTCHA_VERIFICATION_URL', None)
    if configured_url:
        return configured_url
    if get_captcha_version() == 2:
        return V2_VERIFICATION_URL
    return V1_VERIFICATION_URL


def get_verification_payload(value):
    if get_captcha_version() == 2:
        return {'response': value}
    return {'solution': value}


def get_verification_headers():
    if get_captcha_version() != 2:
        return {}

    api_key = getattr(settings, 'FRC_CAPTCHA_API_KEY', None)
    return {'X-API-Key': api_key} if api_key else {}


def get_widget_script_urls():
    module_js = getattr(settings, 'FRC_WIDGET_MODULE_JS', None)
    classic_js = getattr(settings, 'FRC_WIDGET_JS', None)

    if module_js and classic_js:
        return module_js, classic_js

    if get_captcha_version() == 2:
        return (
            module_js or V2_WIDGET_MODULE_JS,
            classic_js or V2_WIDGET_JS,
        )

    return (
        module_js or V1_WIDGET_MODULE_JS,
        classic_js or V1_WIDGET_JS,
    )


def get_widget_language_attr():
    return 'lang' if get_captcha_version() == 2 else 'data-lang'


def get_widget_field_name_attr():
    return 'data-form-field-name' if get_captcha_version() == 2 else 'data-solution-field-name'
