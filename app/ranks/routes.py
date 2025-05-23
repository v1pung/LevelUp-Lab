from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from flask_login import login_required, current_user

from .forms import ActivityForm
from .model import Activity, RankHistory
from .. import db
from ..auth.model import Users
from ..utils import get_next_needed_xp, get_rank_name, get_rank_code, count_completed_tasks, get_daily_mmr_sum

ranks = Blueprint('ranks', __name__, template_folder='templates', static_folder='static')


@ranks.route("/")
def index():
    return render_template("ranks/index.html", title="Главная")


@ranks.route("/stats", methods=['GET', 'POST'])
@login_required
def stats():
    activities = Activity.query.filter_by(owner=current_user.id)

    next_xp = get_next_needed_xp(current_user.rank)
    rank_name = get_rank_name(current_user.rank)
    history = get_daily_mmr_sum(current_user.id)
    rank_code = get_rank_code(rank_name)

    return render_template("ranks/stats.html", title="Статистика", activities=activities, next_xp=next_xp,
                           history=history, rank_name=rank_name, rank_code=rank_code)


@ranks.route("/activities", methods=['GET', 'POST'])
@login_required
def activities():
    form = ActivityForm()
    activities = Activity.query.filter_by(owner=current_user.id).all()
    if form.validate_on_submit():
        if len(activities) >= 6:
            flash('Максимальное количество активностей - 6. Удалите старые перед созданием новых.', 'error')
            return redirect(url_for('ranks.activities'))

        activity = Activity(name=form.name.data, reward=form.reward.data, owner=current_user.id)
        try:
            db.session.add(activity)
            db.session.commit()
            flash(f'created successfully!', "success")
        except Exception as e:
            print("Ошибка БД " + str(e))
            flash("DB error", "error")
        return redirect(url_for('ranks.activities'))
    return render_template("ranks/activities.html", title="Активности", form=form, activities=activities)


@ranks.route('/save_activities', methods=['POST'])
@login_required
def save_activities():
    selected_activities = request.form.getlist('completed_activities')
    selected_activities = list(map(int, selected_activities))

    activities = Activity.query.filter_by(owner=current_user.id).all()
    for activity in activities:
        activity.is_completed = activity.id in selected_activities

    try:
        db.session.commit()
        flash("Сохранено!", "success")
    except Exception as e:
        print("BD ERROR " + str(e))
    return redirect(url_for('ranks.stats'))


@ranks.route("/activities/<int:id>/delete", methods=["POST"])
@login_required
def delete_activity(id):
    activity = Activity.query.get(id)

    if activity.owner != current_user.id:
        abort(403)

    try:
        RankHistory.query.filter_by(activity_id=activity.id).update({
            'activity_name': activity.name,
            'activity_id': None
        })
        db.session.delete(activity)
        db.session.commit()
        return redirect(url_for('ranks.activities'))
    except Exception as e:
        db.session.rollback()
        print("Ошибка в БД " + str(e))
    return redirect(url_for('ranks.activities'))


@ranks.route("/leaderboard", methods=["GET"])
def leaderboard():
    users = Users.query.order_by(Users.rank.desc()).limit(10).all()
    ranking_dict = {user.id: get_rank_name(user.rank) for user in users}
    return render_template("ranks/leaderboard.html", users=users,
                           ranking_dict=ranking_dict, count_completed_tasks=count_completed_tasks)
