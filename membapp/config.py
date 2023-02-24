class Config:
    AMIN_EMAIL='admin@memba.com'
    SECRET_KEY='4P)1D710k'

class LiveConfig(Config):
    AMIN_EMAIL='admin@memba.com'
    SERVER_ADDRESS='https://server.memba.com'

class TestConfig(Config):
    SERVER_ADDRESS='http://127.0.0.1:8085'

