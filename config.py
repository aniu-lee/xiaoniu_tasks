import os

from kombu import Exchange, Queue

from configs import configs

basedir = os.path.abspath(os.path.dirname(__file__))

configss = configs()

class Config:
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_DEFAULT_QUEUE = 'default'
    CELERY_DEFAULT_EXCHANGE = 'default'
    CELERY_DEFAULT_ROUTING_KEY = 'default'

    CELERY_ACKS_LATE = True
    CELERYD_PREFETCH_MULTIPLIER = 1

    CELERY_QUEUES = (
        Queue("default", Exchange("default","direct"), routing_key="default"),
        Queue("prioritys", Exchange("prioritys","direct"), routing_key="prioritys", queue_arguments={'x-max-priority': 9})
    )

    CONFIGS = configss

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    CELERY_BROKER_URL = Config.CONFIGS.get('celery_broker_url')
    CELERY_RESULT_BACKEND = None
    # CELERY_BROKER_URL = 'amqp://admin:admin@127.0.0.1:5672//'
    CELERYD_MAX_TASKS_PER_CHILD = 5000
    SQLALCHEMY_DATABASE_URI = Config.CONFIGS.get('celery_job_log_db_url')


class ProductionConfig(Config):
    DEBUG = False
    CELERY_BROKER_URL = Config.CONFIGS.get('celery_broker_url')
    CELERY_RESULT_BACKEND = None
    CELERYD_MAX_TASKS_PER_CHILD = 5000
    SQLALCHEMY_DATABASE_URI = Config.CONFIGS.get('celery_job_log_db_url')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
