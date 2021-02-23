from .main import create_app, task_queue

app = create_app

app = create_app()
app.app_context().push()