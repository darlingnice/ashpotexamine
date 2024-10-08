
# CORS setting

CORS_ALLOW_CREDENTIALS = True

FRONTEND_SERVER_PORT = '5500'
FRONTEND_EMAIL_HTML = ""
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1',
  
]


CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    'CONNECT',
    'HEAD',
    'TRACE',
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-custom-header",
]
