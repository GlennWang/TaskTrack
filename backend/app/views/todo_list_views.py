# views/todo_list_views.py
from flask import request
from flask.views import MethodView
from extensions import db
from models import ToDoList

class ToDoListApi(MethodView):
    def get(self, item_id):
        if not item_id:
            items = ToDoList.query.all()
            results = [
                {
                    'id': item.id,
                    'name': item.name,
                    'priority': item.priority,
                    'importance': item.importance
                } for item in items
            ]
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
        item = ToDoList.query.get(item_id)
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': {
                'id': item.id,
                'name': item.name,
                'priority': item.priority,
                'importance': item.importance
            }
        }

    def post(self):
        form = request.json
        item = ToDoList(
            name=form.get('name'),
            priority=form.get('priority', 1),
            importance=form.get('importance', 1)
        )
        db.session.add(item)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据添加成功',
        }

    def delete(self, item_id):
        item = ToDoList.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功',
        }

    def put(self, item_id):
        item = ToDoList.query.get(item_id)
        item.name = request.json.get('name')
        item.priority = request.json.get('priority', item.priority)
        item.importance = request.json.get('importance', item.importance)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功',
        }

todo_list_view = ToDoListApi.as_view('todo_list_api')
