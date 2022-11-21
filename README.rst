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

Add the script tags from Friendly Captcha to your forms template
(see https://docs.friendlycaptcha.com/#/installation)

.. code-block::

    <script type="module" src="https://unpkg.com/friendly-challenge@0.9.8/widget.module.min.js" async defer></script>
    <script nomodule src="https://unpkg.com/friendly-challenge@0.9.8/widget.min.js" async defer></script>

I thought about adding these static assets as form media assets, but
users wouldn't be able to choose the desired version. So I decided
against for now.

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
