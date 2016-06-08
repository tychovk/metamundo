import celery
import config

cel_app = celery.Celery('test', broker='CELERY_BROKER_URL')
cel_app.config_from_object('config.celery_config')