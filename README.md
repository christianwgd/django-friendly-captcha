# Django Friendly Captcha

[![image](https://img.shields.io/pypi/v/django-friendly-captcha)](https://pypi.python.org/pypi/django-friendly-captcha)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/django-friendly-captcha)](https://pypi.python.org/pypi/django-friendly-captcha)
[![image](https://codecov.io/gh/christianwgd/django-friendly-captcha/graph/badge.svg?token=CJ39YW793C)](https://codecov.io/gh/christianwgd/django-friendly-captcha)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Django field/widget for Friendly Captcha
(<https://friendlycaptcha.com>).

# Installation

Latest version:

> pip install -e
> git+git://github.com/christianwgd/django-friendly-captcha.git#egg=django-friendly-captcha

Stable version:

> pip install django-friendly-captcha

# Documentation

## Usage

Add \'friendly_captcha\' to your INSTALLED_APPS.

``` 
INSTALLED_APPS = [
    ...
    'friendly_captcha',
]
```

Add the captcha field to your form:

``` 
from friendly_captcha.fields import FrcCaptchaField


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = (
            'name', 'email', 'subject', 'text'
        )

    captcha = FrcCaptchaField()
```

As of version 0.1.7 the javascript static assets are included in the
widget, so there is no need to do that in your project templates.
Version 0.1.10 includes friendly captcha version 0.9.15 javascript
files. If you need a different version you can set these by providing
them in your settings:

``` 
FRC_WIDGET_MODULE_JS = 'https://unpkg.com/friendly-challenge@0.9.8/widget.module.min.js'
FRC_WIDGET_JS = 'https://unpkg.com/friendly-challenge@0.9.8/widget.min.js'
```

For version 0.1.6 and below you need to include the script tags from
Friendly Captcha to your forms template (see
<https://docs.friendlycaptcha.com/#/installation>)

``` 
<script type="module" src="https://unpkg.com/friendly-challenge@0.9.8/widget.module.min.js" async defer></script>
<script nomodule src="https://unpkg.com/friendly-challenge@0.9.8/widget.min.js" async defer></script>
```

If you build up your form from single fields, dont\'t forget to include
the captcha form field.

## Configuration

>[!NOTE] 
>FRC_CAPTCHA_VERSION defaults to \'1\', so if you omit this setting or
set to None, v1 is used. There's no need to take any action if you stick 
to version 1.

### v1

Register to Friendly Captcha at <https://friendlycaptcha.com/signup> to
get your site key and captcha secret.

``` 
FRC_CAPTCHA_VERSION = 1  # or '1'
FRC_CAPTCHA_SECRET = '<yourCaptchaSecret'
FRC_CAPTCHA_SITE_KEY = '<yourCaptchaSiteKey>'
```

There\'s no need to specif the captcha verification URL anymore, this
is handled automatically.

### v2

Instead of a secret you now get new API-Key with your registration. If 
you're already registered reach out to the friendly-captcha Website to 
get your API-Key.

``` 
FRC_CAPTCHA_VERSION = 2  # or '2'
FRC_CAPTCHA_API_KEY = '<yourCaptchaApiKey'
FRC_CAPTCHA_SITE_KEY = '<yourCaptchaSiteKey>'
```

There\'s also a new setting to specify the endpoint region (\"EU\" or
\"global\"). Please note that you need to have a special plan to
choose a special endpoint. (See the [friendly captcha
docs](https://friendlycaptcha.com) for more information).

``` 
FRC_CAPTCHA_ENDPOINT = 'eu | global'
```

The setting defaults to \'global\'.

In default the form will fail with an error (\'Captcha test failed\').
You can change this behaviour by setting FRC_CAPTCHA_FAIL_SILENT to
True.

``` 
FRC_CAPTCHA_FAIL_SILENT = False
```

When setting FAIL_SILENT to True it\'s up to you to handle captcha
verification:

``` 
# in your form view
def form_valid(self, form):
    captcha_verified = form.cleaned_data['captcha']
    if captcha_verified:
        # send mail or whatever ...
    else:
        # captcha verification failed, do nothing ...
```

If the captcha response returns with some http code other than 200, that
doesn\'t mean the captcha result is invalid, it simply wasn\'t able ot
resolve the puzzle (because i.e. the friendly-captcha server is down or
there are network problems). You can specify how to deal with those
responses by setting

``` 
FRC_CAPTCHA_ACCEPT_UNVERIFIED = False|True
```

FRC_CAPTCHA_ACCEPT_UNVERIFIED defaults to False.

As of version 0.1.11 there\'s a new settings option to get a mocked
value from the captcha verification. You can set
FRC_CAPTCHA_MOCKED_VALUE to True or False, depending on the value you
need for testing. The default value is unset which equals to None.

``` 
FRC_CAPTCHA_MOCKED_VALUE = None|False|True
```

## Custom widget attributes

You can add custom widget attrs to the FrcCaptchaField like in any other
Django field:

``` 
captcha = FrcCaptchaField(widget=FrcCaptchaWidget(attrs={'data-theme': 'dark'}))
```

See <https://docs.friendlycaptcha.com/#/widget_api> for additional
widget attrs. The data-lang attr is set from your Django configured
language.

## Logging

If you want to log the results of the captcha verifications you can add
a logger to your logging configuration:

``` 
'django.friendly_captcha': {
    'handlers': ['default'],
    'level': 'INFO',
}
```
