from datetime import datetime

from flask_apscheduler import APScheduler

from .auth.model import Users
from .extensions import db
from .ranks.model import RankHistory, Activity

scheduler = APScheduler()


def save_xp():
    """Function to be done at 00:00 to save users XP income"""
    with scheduler.app.app_context():
        today = datetime.now().date()
        users = Users.query.all()

        for user in users:
            compl_activities = Activity.query.filter_by(owner=user.id, is_completed=True).all()
            total_xp = sum(activity.reward for activity in compl_activities) if compl_activities else -5

            if total_xp < 0 and user.rank < 5:
                user.rank += 0
            else:
                user.rank += total_xp

            for activity in compl_activities:
                existing_activity = RankHistory.query.filter_by(activity_id=activity.id, user_id=user.id, date=today).first()
                if not existing_activity:
                    new_entry = RankHistory(user_id=user.id, activity_id=activity.id, date=today, value=activity.reward)
                    db.session.add(new_entry)

            try:
                db.session.commit()
                print(f"[{datetime.now()}] XP сохранены для пользователя {user.id}.")
            except Exception as e:
                db.session.rollback()
                print("BD ERROR " + str(e))

            # Сброс completed статусов
            for activity in compl_activities:
                activity.is_completed = False
            db.session.commit()



scheduler.add_job(id='save_xp_job', func=save_xp, trigger='cron', hour=23, minute=59, misfire_grace_time=60)
