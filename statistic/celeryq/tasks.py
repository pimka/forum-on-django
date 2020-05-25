from uuid import UUID
from .celery import app
from .exceptions import ConnectionError
from .requester import user_stats, head_stats, mes_stats

TASK_KWARGS = {'autoretry_for': (ConnectionError,), 'retry_kwargs': {
    'max_retries': 5}, 'retry_backoff': True}
TEMPLATE = '{0}.{1}.{2}'
MODULE = 'task'
SPACE = 'statistic'

#celery -A celeryq worker -l info

def send_stats(data, requester):
    data, code = requester(data)

    if code == 503:
        raise ConnectionError

    return data, code

@app.task(**TASK_KWARGS, name=TEMPLATE.format(MODULE, SPACE, 'user'))
def send_user_stats(user, action, input, output):
    data = {
        'user_uuid': user,
        'operation': action,
        'before_changes': input,
        'after_changes': output,
    }

    data, code = send_stats(data, user_stats)
    return (data, code)

@app.task(**TASK_KWARGS, name=TEMPLATE.format(MODULE, SPACE, 'heading'))
def send_head_stats(user, action, input, output):
    data = {
        'user_uuid': user,
        'operation': action,
        'before_changes': input,
        'after_changes': output,
    }

    data, code = send_stats(data, head_stats)
    return (data, code)

@app.task(**TASK_KWARGS, name=TEMPLATE.format(MODULE, SPACE, 'message'))
def send_mes_stats(user, action, input, output):
    data = {
        'user_uuid': user,
        'operation': action,
        'before_changes': input,
        'after_changes': output,
    }

    data, code = send_stats(data, mes_stats)
    return (data, code)