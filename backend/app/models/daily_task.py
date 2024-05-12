from extensions import db
from sqlalchemy.exc import IntegrityError

class DailyTask(db.Model):
    __tablename__ = 'daily_task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    @staticmethod
    def init_db():
        tasks = [
            ('Daily Task 1',),
            ('Daily Task 2',)
        ]
        for task in tasks:
            daily_task = DailyTask(
                name=task[0]
            )
            db.session.add(daily_task)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate daily task found: {task[0]}")