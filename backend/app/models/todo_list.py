from extensions import db
from sqlalchemy.exc import IntegrityError

class ToDoList(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=1)
    importance = db.Column(db.Integer, default=1)

    @staticmethod
    def init_db():
        items = [
            ('To Do 1', 1, 1),
            ('To Do 2', 2, 2)
        ]
        for item in items:
            to_do = ToDoList(
                name=item[0],
                priority=item[1],
                importance=item[2]
            )
            db.session.add(to_do)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate to-do item found: {item[0]}")
