from collections import defaultdict
import os.path
import secrets
from PIL import Image
from flask import current_app
from .ranks.model import RankHistory


class Ranks_XP:
    # 22 total ranks, 30xp needed for each
    xp_thresholds = [i for i in range(0, 660, 30)]
    # b1, b2, b3, s1, s2, s3, g1, g2, g3, p1, p2, p3, d1, d2, d3, c1, c2, c3, gc1, gc2, gc3, ssl = _xp_thresholds
    rank_names = {x: y for x, y in zip(xp_thresholds, ['Bronze 1', 'Bronze 2', 'Bronze 3',
                                                       'Silver 1', 'Silver 2', 'Silver 3',
                                                       'Gold 1', 'Gold 2', 'Gold 3',
                                                       'Plat 1', 'Plat 2', 'Plat 3',
                                                       'Diamond 1', 'Diamond 2', 'Diamond 3',
                                                       'Champ 1', 'Champ 2', 'Champ 3',
                                                       'Grand champ 1', 'Grand champ 2', 'Grand champ 3',
                                                       'SSL'])}


rank_obj = Ranks_XP()


def get_rank_name(xp: int) -> str:
    """Возвращает название ранга по количеству XP"""
    global rank_obj

    if not isinstance(xp, int):
        raise ValueError("XP must be integer")

    # Находим максимальный порог, который меньше или равен переданному XP
    matching_threshold = max(
        (threshold for threshold in rank_obj.rank_names.keys() if threshold <= xp),
        default=0
    )

    return rank_obj.rank_names[matching_threshold]


def get_next_needed_xp(current_xp):
    global rank_obj
    next_xp = next(x for x in rank_obj.xp_thresholds if x > current_xp)
    return next_xp


def get_daily_mmr_sum(user_id):
    entries = RankHistory.query.filter_by(user_id=user_id).order_by(RankHistory.date.desc()).all()

    daily_sums = defaultdict(int)

    for entry in entries:
        daily_sums[entry.date] += entry.value

    return daily_sums


def get_rank_code(rank_name):
    mapping = {
        "Bronze": "b",
        "Silver": "s",
        "Gold": "g",
        "Platinum": "p",
        "Diamond": "d",
        "Сhamp": "c",
        "Grand champ": "gc",
        "SSL": "ssl"
    }

    parts = rank_name.split()
    if len(parts) == 2:
        tier, level = parts
        tier_code = mapping.get(tier.capitalize(), "unknown")
        return f"{tier_code}{level}"
    elif parts[0] == "SSL":
        return f"ssl"
    return "unknown"


def count_completed_tasks(current_user_id):
    compl_tasks = RankHistory.query.filter_by(user_id=current_user_id).count()
    return compl_tasks


def save_picture(pic):
    if pic:
        random_hex = secrets.token_hex(8)
        _, ext = os.path.splitext(pic.filename)
        pic_name = random_hex + ext
        picture_path = os.path.join(current_app.config['SERVER_PATH'], pic_name)
        output_size = (125, 125)
        i = Image.open(pic)
        i.thumbnail(output_size)
        i.save(picture_path)
        return pic_name
    return ''
