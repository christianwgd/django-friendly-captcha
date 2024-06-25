Django Friendly Captcha
=======================

.. image:: https://img.shields.io/pypi/v/django-friendly-captcha
    :target: https://pypi.python.org/pypi/django-friendly-captcha

.. image:: https://img.shields.io/pypi/dm/django-friendly-captcha
    :alt: PyPI - Downloads
    :target: https://pypi.python.org/pypi/django-friendly-captcha

Django field/widget for Friendly Captcha (https://friendlycaptcha.com).



Installation
------------

Latest version:

    pip install -e git+git://github.com/christianwgd/django-friendly-captcha.git#egg=django-friendly-captcha

Stable version:

    pip install django-friendly-captcha

Documentation
-------------

Usage
#####

Add 'friendly_captcha' to your INSTALLED_APPS.

.. code-block::

    INSTALLED_APPS = [
        ...
        'friendly_captcha',
    ]

Add the captcha field to your form:

.. code-block::

    from friendly_captcha.fields import FrcCaptchaField


    class ContactForm(forms.ModelForm):

        class Meta:
            model = ContactMessage
            fields = (
                'name', 'email', 'subject', 'text'
            )

        captcha = FrcCaptchaField()

As of version 0.1.7 the javascript static assets are included in
the widget, so there is no need to do that in your project templates.
Version 0.1.10 includes friendly captcha version 0.9.16 javascript files.
If you need a different version you can set these by providing
them in your settings:

.. code-block::

    FRC_WIDGET_MODULE_JS = 'https://unpkg.com/friendly-challenge@0.9.8/widget.module.min.js'
    FRC_WIDGET_JS = 'https://unpkg.com/friendly-challenge@0.9.8/widget.min.js'

For version 0.1.6 and below you need to include the script tags from
Friendly Captcha to your forms template
(see https://docs.friendlycaptcha.com/#/installation)

.. code-block::

    <script type="module" src="https://unpkg.com/friendly-challenge@0.9.8/widget.module.min.js" async defer></script>
    <script nomodule src="https://unpkg.com/friendly-challenge@0.9.8/widget.min.js" async defer></script>

If you build up your form from single fields, dont't forget to include
the captcha form field.

Configuration
#############

Register to Friendly Captcha at https://friendlycaptcha.com/signup to get your
sitekey and captcha secret.

.. code-block::

    FRC_CAPTCHA_SECRET = '<yourCaptchaSecret'
    FRC_CAPTCHA_SITE_KEY = '<yourCaptchaSiteKey>'

.. code-block::

    FRC_CAPTCHA_VERIFICATION_URL = 'https://api.friendlycaptcha.com/api/v1/siteverify'

In default the form will fail with an error ('Captcha test failed'). You can change
this behaviour by setting FRC_CAPTCHA_FAIL_SILENT to True.

.. code-block::

    FRC_CAPTCHA_FAIL_SILENT = False

When setting FAIL_SILENT to True it's up to you to handle captcha verification:

.. code-block::

    # in your form view
    def form_valid(self, form):
        captcha_verified = form.cleaned_data['captcha']
        if captcha_verified:
            # send mail or whatever ...
        else:
            # captcha verification failed, do nothing ...

As of version 0.1.11 there's a new settings option to get a mocked
value from the captcha verification. You can set FRC_CAPTCHA_MOCKED_VALUE
to True or False, depending on the vaule you need for testing.
The default value is unset which equals to None.

.. code-block::

    FRC_CAPTCHA_MOCKED_VALUE = None|False|True

Custom widget attributes
########################

You can add custom widget attrs to the FrcCaptchaField like in any other
Django field:

.. code-block::

    captcha = FrcCaptchaField(widget=FrcCaptchaWidget(attrs={'data-start': 'auto'}))

See https://docs.friendlycaptcha.com/#/widget_api for additional widget attrs.
The data-lang attr is set from your Django configured language.

Logging
#######

If you want to log the results of the captcha verifications you can
add a logger to your logging configuration:

.. code-block::

    'django.friendly_captcha': {
        'handlers': ['default'],
        'level': 'INFO',
    }
