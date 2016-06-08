#!usr/bin/env python3
# config.py
from datetime import timedelta



# Celery config
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=60),

    },
}
IS_ASYNC = True


"""
#!usr/bin/env python3
# config.py
from datetime import timedelta



# Celery config
celery_config = {
'CELERY_BROKER_URL' : 'redis://localhost:6379/0',
'CELERY_RESULT_BACKEND' : 'redis://localhost:6379/0',
'CELERY_TASK_RESULT_EXPIRES' : 3600,
'CELERYBEAT_SCHEDULE' : {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=60),

    },
},
'IS_ASYNC': True }
"""