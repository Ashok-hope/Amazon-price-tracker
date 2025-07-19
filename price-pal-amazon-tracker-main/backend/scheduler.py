
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from price_checker import price_checker
from firebase_config import firebase_service
from email_service import send_weekly_reminder_email
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def check_all_prices():
    """Scheduled task to check all product prices"""
    logger.info("Starting scheduled price check...")
    try:
        await price_checker.check_all_products()
        logger.info("Completed scheduled price check")
    except Exception as e:
        logger.error(f"Error in scheduled price check: {e}")

async def send_weekly_reminders():
    """Send weekly reminders to all users"""
    logger.info("Sending weekly reminders...")
    try:
        # Get all users
        users_collection = firebase_service.get_collection("users")
        users = users_collection.stream()
        
        for user_doc in users:
            user_data = user_doc.to_dict()
            await send_weekly_reminder_email(user_data["email"], user_data["name"])
        
        logger.info("Completed sending weekly reminders")
    except Exception as e:
        logger.error(f"Error sending weekly reminders: {e}")

def start_scheduler():
    """Start the scheduler with all tasks"""
    try:
        # Check prices 6 times a day (0, 4, 8, 12, 16, 20 IST)
        scheduler.add_job(
            check_all_prices,
            CronTrigger(hour='0,4,8,12,16,20', minute=0, timezone='Asia/Kolkata'),
            id='price_check',
            name='Check product prices',
            replace_existing=True
        )
        
        # Send weekly reminders every Sunday at 10 AM IST
        scheduler.add_job(
            send_weekly_reminders,
            CronTrigger(day_of_week='sun', hour=10, minute=0, timezone='Asia/Kolkata'),
            id='weekly_reminders',
            name='Send weekly reminders',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("Scheduler started successfully")
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")

def stop_scheduler():
    """Stop the scheduler"""
    try:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
