import os
from flask import Flask
from extensions import cors, db
from views import task_inventory_view, daily_task_view, todo_list_view
from models import TaskInventory, DailyTask, ToDoList

app = Flask(__name__)

# 設置資料庫連線
db_path = os.path.join(os.getcwd(), 'database', 'tasktrack.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫實例
db.init_app(app)
cors.init_app(app)

@app.cli.command()
def create():
    """
    [test] Initialize the database and set up tables.
    """
    db.drop_all()
    db.create_all()
    TaskInventory.init_db()
    DailyTask.init_db()
    ToDoList.init_db()

@app.route('/')
def hello_world():
    return 'hello world!'

# 註冊task_inventory_view
app.add_url_rule('/tasks/', defaults={'task_id': None},
                 view_func=task_inventory_view, methods=['GET', ])
app.add_url_rule('/tasks/',
                 view_func=task_inventory_view, methods=['POST',])
app.add_url_rule('/tasks/<int:task_id>', view_func=task_inventory_view, methods=['GET', 'PUT', 'DELETE'])

# 註冊daily_task_view
app.add_url_rule('/daily_tasks/', defaults={'task_id': None},
                 view_func=daily_task_view, methods=['GET', ])
app.add_url_rule('/daily_tasks/',
                 view_func=daily_task_view, methods=['POST',])
app.add_url_rule('/daily_tasks/<int:task_id>', view_func=daily_task_view, methods=['GET', 'PUT', 'DELETE'])

# 註冊todo_list_view
app.add_url_rule('/todo_lists/', defaults={'task_id': None},
                 view_func=todo_list_view, methods=['GET', ])
app.add_url_rule('/todo_lists/',
                 view_func=todo_list_view, methods=['POST',])
app.add_url_rule('/todo_lists/<int:task_id>', view_func=todo_list_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)