from apscheduler.schedulers.asyncio import AsyncIOScheduler
from notification.notification_handler import check_and_send_reminders


def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # Проверяем каждые 60 минут
    scheduler.add_job(
        check_and_send_reminders,
        'interval',
        minutes=60,
        args=[bot]
    )

    return scheduler