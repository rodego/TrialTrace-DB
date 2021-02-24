web: gunicorn wsgi.py
worker: celery -A app.queue_worker.task_queue worker -l INFO