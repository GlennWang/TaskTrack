# views/task_inventory_views.py
from flask import request
from flask.views import MethodView
from extensions import db
from models import TaskInventory

class TaskInventoryApi(MethodView):
    def get(self, task_id=None):
        if task_id is None:
            tasks = TaskInventory.query.order_by(TaskInventory.priority.asc(), TaskInventory.importance.asc()).all()
            results = [
                {
                    'id': task.id,
                    'category': task.category,
                    'name': task.name,
                    'description': task.description,
                    'priority': task.priority,
                    'importance': task.importance,
                    'deadline': task.deadline
                } for task in tasks
            ]
            return {
                'status': 'success',
                'message': '資料查詢成功',
                'results': results
            }
        task = TaskInventory.query.get(task_id)
        if task:
            return {
                'status': 'success',
                'message': '資料查詢成功',
                'results': {
                    'id': task.id,
                    'category': task.category,
                    'name': task.name,
                    'description': task.description,
                    'priority': task.priority,
                    'importance': task.importance,
                    'deadline': task.deadline
                }
            }
        else:
            return {
                'status': 'error',
                'message': 'Task not found'
            }, 404

    def post(self):
        form = request.json
        task = TaskInventory(
            name=form.get('name'),
            category=form.get('category'),
            description=form.get('description'),
            priority=form.get('priority'),
            importance=form.get('importance'),
            deadline=form.get('deadline')
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
        task.category = request.json.get('category')
        task.description = request.json.get('description')
        task.priority = request.json.get('priority')
        task.importance = request.json.get('importance')
        task.deadline = request.json.get('deadline')
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料修改成功',
        }

task_inventory_view = TaskInventoryApi.as_view('task_api')