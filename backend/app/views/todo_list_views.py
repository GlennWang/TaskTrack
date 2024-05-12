# views/todo_list_views.py
from flask import request
from flask.views import MethodView
from extensions import db
from models import ToDoList

class ToDoListApi(MethodView):
    def get(self, task_id):
        if not task_id:
            tasks = ToDoList.query.all()
            results = [
                {
                    'id': task.id,
                    'name': task.name,
                    'status': task.status
                } for task in tasks
            ]
            return {
                'status': 'success',
                'message': '資料查詢成功',
                'results': results
            }
        task = ToDoList.query.get(task_id)
        return {
            'status': 'success',
            'message': '資料查詢成功',
            'results': {
                'id': task.id,
                'name': task.name,
                'status': task.status
            }
        }

    def post(self):
        form = request.json
        task = ToDoList(
            name=form.get('name')
        )
        db.session.add(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料添加成功',
        }

    def delete(self, task_id):
        task = ToDoList.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料刪除成功',
        }

    def put(self, task_id):
        task = ToDoList.query.get(task_id)
        form = request.json
        name = form.get('name')
        status = form.get('status')

        if name is not None:
            task.name = name
        elif status is not None:
            task.status = status

        db.session.commit()
        return {
            'status': 'success',
            'message': '資料修改成功',
        }

todo_list_view = ToDoListApi.as_view('todo_list_api')