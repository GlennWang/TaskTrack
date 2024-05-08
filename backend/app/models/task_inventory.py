from extensions import db
from sqlalchemy.exc import IntegrityError

class TaskInventory(db.Model):
    __tablename__ = 'task_inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    importance = db.Column(db.Integer, nullable=False)

    @staticmethod
    def init_db():
        items = [
            ('Task 1', 1, 1),
            ('Task 2', 2, 3),
            ('Task 3', 3, 2)
        ]
        for item in items:
            task = TaskInventory(
                name=item[0],
                priority=item[1],
                importance=item[2]
            )
            db.session.add(task)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate task found: {item[0]}")
