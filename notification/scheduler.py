from apscheduler.schedulers.asyncio import AsyncIOScheduler
from notification.notification_handler import check_and_send_reminders


def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # Проверяем каждые 5 минут
    scheduler.add_job(
        check_and_send_reminders,
        'interval',
        minutes=1,
        args=[bot]
    )

    return scheduler