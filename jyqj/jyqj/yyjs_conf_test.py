# -*- coding: UTF-8 -*-
import os

APP_LOG_DIR = '/tmp/admin_server'
DEBUG = True

NGINX_URL_PREFIX = 'http://192.168.1.99:9090/'
OSS_UPLOAD_FILE_PATH = 'http://admin-uploadfiles-yyjs.oss-cn-beijing.aliyuncs.com/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yyjs_test',
        # 'USER': 'admin',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.1.99',
        # 'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
            # "charset": "utf8mb4",
        },
        "ATOMIC_REQUESTS": True,
    },
}

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = ''

RELEASE = 'test'

if RELEASE == 'test':
    OSSCONF_OSS_ID = '..'
    OSSCONF_OSS_SECRET = '...'
    OSSCONF_BUCKET_KEY = 'yyjs-test'
    OSSCONF_END_POINT = 'http://oss-cn-beijing.aliyuncs.com'
    OSS_UPLOAD_FILE_PATH = 'http://yyjs-test.oss-cn-beijing.aliyuncs.com/'


elif RELEASE == 'online':
    OSSCONF_OSS_ID = '..'
    OSSCONF_OSS_SECRET = '...'
    OSSCONF_BUCKET_KEY = 'yyjs-online'
    OSSCONF_END_POINT = 'http://oss-cn-beijing.aliyuncs.com'
    OSS_UPLOAD_FILE_PATH = 'http://yyjs-online.oss-cn-beijing.aliyuncs.com/'

elif RELEASE == 'me':
    OSSCONF_OSS_ID = '..'
    OSSCONF_OSS_SECRET = '...'
    OSSCONF_BUCKET_KEY = 'admin-uploadfiles-yyjs'
    OSSCONF_END_POINT = 'http://oss-cn-beijing.aliyuncs.com'
    OSS_UPLOAD_FILE_PATH = 'http://admin-uploadfiles-yyjs.oss-cn-beijing.aliyuncs.com/'


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#
#     'formatters': {
#         'verbose': {
#             'format': '%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#         'profile': {
#             'format': '%(asctime)s %(message)s'
#         }
#     },
#
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#         'default': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(APP_LOG_DIR, 'default.log'),
#             'formatter': 'verbose',
#         },
#         'info_handler': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(APP_LOG_DIR, 'info.log'),
#             'formatter': 'verbose',
#         },
#         'error_handler': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(APP_LOG_DIR, 'error.log'),
#             'formatter': 'verbose',
#         },
#         'profile_handler': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(APP_LOG_DIR, 'profile.log'),
#             'formatter': 'profile',
#         },
#     },
#
#     'loggers': {
#         'django': {
#             'handlers': ['default'],
#             'propagate': True,
#             'level': 'INFO',
#         },
#         'django.request': {
#             'handlers': ['error_handler'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'info_logger': {
#             'handlers': ['info_handler', 'console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'error_logger': {
#             'handlers': ['error_handler'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'profile_logger': {
#             'handlers': ['profile_handler'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#
#     }
# }
