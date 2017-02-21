import os

SECRET_KEY = 'some key'

SSL = True

SSL_CERT_PATH = os.path.join(os.path.dirname(__file__),
                             'sample_ssl.cert')
SSL_KEY_PATH = os.path.join(os.path.dirname(__file__),
                            'sample_ssl.key')

DB_URI = 'sqlite:///ircb.db'

SUBSCRIBER_ENDPOINTS = {
    'stores': 'tcp://127.0.0.1:35000',
}

LOGLEVEL = 'INFO'

LOGGING_CONF = dict(
    version=1,
    level=LOGLEVEL,
    formatters=dict(
        bare={
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "[%(asctime)s][%(name)10s %(levelname)7s] %(message)s"
        },
    ),
    handlers=dict(
        console={
            "class": "logging.StreamHandler",
            "formatter": "bare",
            "level": LOGLEVEL,
            "stream": "ext://sys.stdout",
        }
    ),
    loggers=dict(
        ircb={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        network={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        bouncer={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        stores={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        dispatcher={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        irc={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        aiohttp={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        publisher={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        raw={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        },
        identd={
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console"],
        }
    ),
)

INTERNAL_HOST = '127.0.0.1'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# A 32 byte string
WEB_SALT = b'c237202ee55411e584f4cc3d8237ff4b'

# Redis keys
REDIS_KEYS = {
    'STORE': 'store',
    'STORE_CLIENTS': 'store_clients'
}
