from datetime import datetime, timedelta

def has_time_passed(past_time: datetime, threshold_minutes: int = 30, now_time: datetime = None) -> bool:
    if now_time is None:
        now_time = datetime.now()

    return now_time > (past_time + timedelta(minutes=threshold_minutes))
