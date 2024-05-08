# views/task_inventory_views.py
from flask import request
from flask.views import MethodView
from extensions import db
from models import TaskInventory

class TaskInventoryApi(MethodView):
    def get(self, task_id):
        if not task_id:
            tasks = TaskInventory.query.all()
            results = [
                {
                    'id': task.id,
                    'name': task.name,
                    'priority': task.priority,
                    'importance': task.importance
                } for task in tasks
            ]
            return {
                'status': 'success',
                'message': '資料查詢成功',
                'results': results
            }
        task = TaskInventory.query.get(task_id)
        return {
            'status': 'success',
            'message': '資料查詢成功',
            'results': {
                'id': task.id,
                'name': task.name,
                'priority': task.priority,
                'importance': task.importance
            }
        }

    def post(self):
        form = request.json
        task = TaskInventory(
            name=form.get('name'),
            priority=form.get('priority'),
            importance=form.get('importance')
        )
        db.session.add(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料添加成功',
        }

    def delete(self, task_id):
        task = TaskInventory.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料刪除成功',
        }

    def put(self, task_id):
        task = TaskInventory.query.get(task_id)
        task.name = request.json.get('name')
        task.priority = request.json.get('priority')
        task.importance = request.json.get('importance')
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料修改成功',
        }

task_inventory_view = TaskInventoryApi.as_view('task_api')
