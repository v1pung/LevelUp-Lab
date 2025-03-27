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
            user.rank += total_xp if user.rank > 5 else 0

            for activity in compl_activities:
                existing_activity = RankHistory.query.filter_by(activity_id=activity.id, date=today).all()
                if not existing_activity:
                    new_entry = RankHistory(user_id=user.id, activity_id=activity.id, date=today, value=activity.reward)

            try:
                db.session.add(new_entry)
                db.session.commit()
                print(f"[{datetime.now()}] XP сохранены для всех пользователей.")
            except Exception as e:
                print("BD ERROR " + str(e))
            else:
                for activity in compl_activities:
                    activity.is_completed = False


scheduler.add_job(id='save_xp_job', func=save_xp, trigger='cron', hour=18, minute=58, misfire_grace_time=60)
