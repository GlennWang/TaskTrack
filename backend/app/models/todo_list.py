from extensions import db
from sqlalchemy.exc import IntegrityError

class ToDoList(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def init_db():
        tasks = [
            ('To Do 1', False),
            ('To Do 2', False)
        ]
        for task in tasks:
            to_do = ToDoList(
                name=task[0],
                status=task[1]
            )
            db.session.add(to_do)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate to-do task found: {task[0]}")