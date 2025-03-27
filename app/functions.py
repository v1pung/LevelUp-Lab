# from auth.model import Users


class Ranks_XP:
    # 22 total ranks, 30xp needed for each
    _xp_thresholds = [i for i in range(0, 660, 30)]
    # b1, b2, b3, s1, s2, s3, g1, g2, g3, p1, p2, p3, d1, d2, d3, c1, c2, c3, gc1, gc2, gc3, ssl = _xp_thresholds


def get_next_needed_xp(current_xp):
    next_xp = next(x for x in Ranks_XP._xp_thresholds if x > current_xp)
    return next_xp


def get_history(user):
    pass
