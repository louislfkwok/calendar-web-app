from flask import Flask
from flask_session import Session
from routes.auth_routes.login import login_bp
from routes.auth_routes.logout import logout_bp
from routes.auth_routes.register import register_bp
from routes.event_routes.handle_event import handle_event_bp
from routes.task_routes.add_task import add_task_bp
from routes.task_routes.allocate_tasks import allocate_tasks_bp
from routes.task_routes.delete_task import delete_task_bp
from routes.task_routes.edit_task import edit_task_bp
from routes.index import index_bp

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.register_blueprint(add_task_bp)
app.register_blueprint(allocate_tasks_bp)
app.register_blueprint(delete_task_bp)
app.register_blueprint(edit_task_bp)
app.register_blueprint(handle_event_bp)
app.register_blueprint(index_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)


if __name__ == '__main__':
    app.run(debug=True)