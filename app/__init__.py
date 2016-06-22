import celery
import config
import redis #necessary???

cel_app = celery.Celery('tasks', broker=config.celery_config.CELERY_BROKER_URL)
cel_app.config_from_object(config.celery_config)

