from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from models.subscription import Subscription_Date_Levels


def setup_end_date_subscription(start_date: datetime, level: int) -> datetime:
    """Установка даты окончания подписки."""
    if level == Subscription_Date_Levels.DAY:
        end_date = start_date + timedelta(days=1)
    elif level == Subscription_Date_Levels.MONTH:
        end_date = start_date + relativedelta(months=1)
    elif level == Subscription_Date_Levels.HALF_YEAR:
        end_date = start_date + relativedelta(months=6)
    elif level == Subscription_Date_Levels.YEAR:
        end_date = start_date + relativedelta(years=1)
    return end_date
