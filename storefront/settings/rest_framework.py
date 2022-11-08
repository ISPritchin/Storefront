REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}