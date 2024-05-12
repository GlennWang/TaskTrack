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
                } for task in tasks
            ]
            return {
                'status': 'success',
                'message': '資料查詢成功',
                'results': results
            }
        task = DailyTask.query.get(task_id)
        return {
            'status': 'success',
            'message': '資料查詢成功',
            'results': {
                'id': task.id,
                'name': task.name,
            }
        }

    def post(self):
        form = request.json
        task = DailyTask(
            name=form.get('name')
        )
        db.session.add(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料添加成功',
        }

    def delete(self, task_id):
        task = DailyTask.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料刪除成功',
        }

    def put(self, task_id):
        task = DailyTask.query.get(task_id)
        task.name = request.json.get('name')
        db.session.commit()
        return {
            'status': 'success',
            'message': '資料修改成功',
        }

daily_task_view = DailyTaskApi.as_view('daily_task_api')