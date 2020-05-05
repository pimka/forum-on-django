from celery import Celery
from celery_queue.config import Config

app = Celery(include=['celeryq.tasks'])
app.config_from_object(Config)

if __name__ == "__main__":
    app.start()