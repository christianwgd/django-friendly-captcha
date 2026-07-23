from django.conf import settings

V1_VERIFICATION_URL = 'https://api.friendlycaptcha.com/api/v1/siteverify'
V1_VERIFICATION_URL_EU = 'https://eu-api.friendlycaptcha.eu/api/v1/siteverify'
V2_VERIFICATION_URL = 'https://global.frcapi.com/api/v2/captcha/siteverify'
V2_VERIFICATION_URL_EU = 'https://eu.frcapi.com/api/v2/captcha/siteverify'

V1_WIDGET_MODULE_JS = 'https://cdn.jsdelivr.net/npm/friendly-challenge@0.9.20/widget.module.min.js'
V1_WIDGET_JS = 'https://cdn.jsdelivr.net/npm/friendly-challenge@0.9.20/widget.min.js'
V1_WIDGET_ENDPOINT_EU = 'https://eu-api.friendlycaptcha.eu/api/v1/puzzle'
V1_WIDGET_ENDPOINT_GLOBAL = 'https://api.friendlycaptcha.com/api/v1/puzzle'

V2_WIDGET_MODULE_JS = 'https://cdn.jsdelivr.net/npm/@friendlycaptcha/sdk/site.min.js'
V2_WIDGET_JS = 'https://cdn.jsdelivr.net/npm/@friendlycaptcha/sdk/site.compat.min.js'


def get_captcha_version():
    configured_version = getattr(settings, 'FRC_CAPTCHA_VERSION', None)
    if configured_version in (1, '1'):
        return 1
    if configured_version in (2, '2'):
        return 2
    return 1  # Default to version 1 if not specified

def get_captcha_endpoint():
    configured_endpoint = getattr(settings, 'FRC_CAPTCHA_ENDPOINT', None)
    if get_captcha_version() == 2: 
        if configured_endpoint == 'eu':
            return configured_endpoint
        else: 
            return 'global'
    else: 
        if configured_endpoint == 'eu':
            return V1_WIDGET_ENDPOINT_EU
        else:
            return V1_WIDGET_ENDPOINT_GLOBAL

def get_verification_url():
    if get_captcha_version() == 2:
        if get_captcha_endpoint() == 'eu':
            return V2_VERIFICATION_URL_EU
        return V2_VERIFICATION_URL
    else:
        if get_captcha_endpoint() == 'eu':
            return V1_VERIFICATION_URL_EU
        return V1_VERIFICATION_URL

def get_start_mode():
    configured_start_mode = getattr(settings, 'FRC_CAPTCHA_START_MODE', None)
    if configured_start_mode in ('auto', 'focus', 'none'):
        return configured_start_mode
    return 'focus'

def get_verification_payload(value):
    if get_captcha_version() == 2:
        return {'response': value}
    return {'solution': value}

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
