# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'haj)2v9_pcav-jpp6!e$_xjgypc!@j0%d+eg@s68^mzxm(9$fj'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'swgoh',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
    }
}


