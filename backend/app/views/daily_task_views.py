# views/daily_task_views.py
from flask import request
from flask.views import MethodView
from extensions import db
from models import DailyTask

class DailyTaskApi(MethodView):
    def get(self, task_id):
        if not task_id:
            tasks = DailyTask.query.all()
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
                'message': '数据查询成功',
                'results': results
            }
        task = DailyTask.query.get(task_id)
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': {
                'id': task.id,
                'name': task.name,
                'priority': task.priority,
                'importance': task.importance
            }
        }

    def post(self):
        form = request.json
        task = DailyTask(
            name=form.get('name'),
            priority=form.get('priority', 1),
            importance=form.get('importance', 1)
        )
        db.session.add(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据添加成功',
        }

    def delete(self, task_id):
        task = DailyTask.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功',
        }

    def put(self, task_id):
        task = DailyTask.query.get(task_id)
        task.name = request.json.get('name')
        task.priority = request.json.get('priority', task.priority)
        task.importance = request.json.get('importance', task.importance)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功',
        }

daily_task_view = DailyTaskApi.as_view('daily_task_api')
