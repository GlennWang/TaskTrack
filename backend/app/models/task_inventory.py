from extensions import db
from sqlalchemy.exc import IntegrityError

class TaskInventory(db.Model):
    __tablename__ = 'task_inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Integer, nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.String(100), nullable=True)

    @staticmethod
    def init_db():
        items = [
            ('Category A', 'Task 1', 'Description 1', 1, 1, '2024-05-15'),
            ('Category B', 'Task 2', 'Description 2', 2, 3, '2024-05-16'),
            ('Category C', 'Task 3', 'Description 3', 3, 2, '2024-05-17')
        ]
        for item in items:
            task = TaskInventory(
                category=item[0],
                name=item[1],
                description=item[2],
                priority=item[3],
                importance=item[4],
                deadline=item[5]
            )
            db.session.add(task)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate task found: {item[1]}")
