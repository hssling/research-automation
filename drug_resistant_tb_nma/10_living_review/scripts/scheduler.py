#!/usr/bin/env python3
"""
Scheduler for Drug-Resistant TB Living Review System
Manages automated execution of literature search, data extraction, and analysis updates
"""

import json
import logging
import schedule
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import sys
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))


class LivingReviewScheduler:
    """Scheduler for automated living review updates"""

    def __init__(self, config_path="../living_review_config.json"):
        """Initialize the scheduler"""
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.jobs = []

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file not found: {config_path}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON in configuration file: {config_path}")
            return None

    def setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        logging.basicConfig(
            level=getattr(logging, log_config.get('level', 'INFO')),
            filename=log_config.get('file', 'scheduler.log'),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def run_literature_search(self):
        """Run automated literature search"""
        self.logger.info("Running scheduled literature search...")

        try:
            result = subprocess.run([
                sys.executable,
                "scripts/auto_search.py"
            ], capture_output=True, text=True, timeout=3600)

            if result.returncode == 0:
                self.logger.info("Literature search completed successfully")
                self.send_notification(
                    "Literature Search Completed",
                    f"Literature search completed successfully.\n\n{result.stdout}"
                )
            else:
                self.logger.error(f"Literature search failed: {result.stderr}")
                self.send_notification(
                    "Literature Search Failed",
                    f"Literature search failed with error:\n\n{result.stderr}",
                    priority="high"
                )

        except subprocess.TimeoutExpired:
            self.logger.error("Literature search timed out")
            self.send_notification(
                "Literature Search Timeout",
                "Literature search exceeded timeout limit",
                priority="high"
            )
        except Exception as e:
            self.logger.error(f"Error running literature search: {e}")
            self.send_notification(
                "Literature Search Error",
                f"Unexpected error in literature search: {e}",
                priority="high"
            )

    def run_data_extraction(self):
        """Run automated data extraction"""
        self.logger.info("Running scheduled data extraction...")

        try:
            result = subprocess.run([
                sys.executable,
                "scripts/auto_extraction.py"
            ], capture_output=True, text=True, timeout=1800)

            if result.returncode == 0:
                self.logger.info("Data extraction completed successfully")
                self.send_notification(
                    "Data Extraction Completed",
                    f"Data extraction completed successfully.\n\n{result.stdout}"
                )
            else:
                self.logger.error(f"Data extraction failed: {result.stderr}")
                self.send_notification(
                    "Data Extraction Failed",
                    f"Data extraction failed with error:\n\n{result.stderr}",
                    priority="high"
                )

        except subprocess.TimeoutExpired:
            self.logger.error("Data extraction timed out")
            self.send_notification(
                "Data Extraction Timeout",
                "Data extraction exceeded timeout limit",
                priority="high"
            )
        except Exception as e:
            self.logger.error(f"Error running data extraction: {e}")
            self.send_notification(
                "Data Extraction Error",
                f"Unexpected error in data extraction: {e}",
                priority="high"
            )

    def run_analysis_update(self):
        """Run automated analysis update"""
        self.logger.info("Running scheduled analysis update...")

        try:
            # This would run the R script for NMA updates
            result = subprocess.run([
                "Rscript",
                "../03_statistical_analysis/real_nma_analysis.py"
            ], capture_output=True, text=True, timeout=3600)

            if result.returncode == 0:
                self.logger.info("Analysis update completed successfully")
                self.send_notification(
                    "Analysis Update Completed",
                    f"Analysis update completed successfully.\n\n{result.stdout}"
                )
            else:
                self.logger.error(f"Analysis update failed: {result.stderr}")
                self.send_notification(
                    "Analysis Update Failed",
                    f"Analysis update failed with error:\n\n{result.stderr}",
                    priority="high"
                )

        except subprocess.TimeoutExpired:
            self.logger.error("Analysis update timed out")
            self.send_notification(
                "Analysis Update Timeout",
                "Analysis update exceeded timeout limit",
                priority="high"
            )
        except Exception as e:
            self.logger.error(f"Error running analysis update: {e}")
            self.send_notification(
                "Analysis Update Error",
                f"Unexpected error in analysis update: {e}",
                priority="high"
            )

    def send_notification(self, subject: str, message: str, priority: str = "normal"):
        """Send email notification"""
        notification_config = self.config.get('notifications', {})

        if not notification_config:
            return

        # Get notification settings based on priority
        if priority == "high":
            recipients = ["research@drugresistanttb-nma.org"]
        else:
            recipients = ["research@drugresistanttb-nma.org"]

        # Create email message
        msg = MimeMultipart()
        msg['From'] = "livingreview@drugresistanttb-nma.org"
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"[Living Review] {subject}"

        # Add message body
        body = f"""
Living Review System Notification

Subject: {subject}
Priority: {priority}
Timestamp: {datetime.now().isoformat()}

Message:
{message}

---
This is an automated message from the Drug-Resistant TB Living Review System.
Contact: Dr Siddalingaiah H S (hssling@yahoo.com)
Institution: Shridevi Institute of Medical Sciences and Research Hospital, Tumakuru
        """

        msg.attach(MimeText(body, 'plain'))

        try:
            # For now, just log the notification
            # In production, this would send actual emails
            self.logger.info(f"Notification: {subject}")
            self.logger.info(f"Recipients: {', '.join(recipients)}")
            self.logger.info(f"Message: {message[:200]}...")

        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

    def setup_schedule(self):
        """Setup the update schedule"""
        schedule_config = self.config.get('schedule', {})

        # Literature search schedule
        if schedule_config.get('literature_search', {}).get('enabled', True):
            search_config = schedule_config['literature_search']
            frequency = search_config.get('frequency', 'weekly')

            if frequency == 'weekly':
                day = search_config.get('day', 'monday')
                time_str = search_config.get('time', '02:00')

                # Schedule for specific day and time
                getattr(schedule.every(), day).at(time_str).do(self.run_literature_search)
                self.logger.info(f"Scheduled literature search for {day} at {time_str}")

        # Data extraction schedule
        if schedule_config.get('data_extraction', {}).get('enabled', True):
            extract_config = schedule_config['data_extraction']
            frequency = extract_config.get('frequency', 'daily')
            time_str = extract_config.get('time', '06:00')

            if frequency == 'daily':
                schedule.every().day.at(time_str).do(self.run_data_extraction)
                self.logger.info(f"Scheduled data extraction daily at {time_str}")

        # Analysis update schedule
        if schedule_config.get('analysis_update', {}).get('enabled', True):
            update_config = schedule_config['analysis_update']
            frequency = update_config.get('frequency', 'biweekly')
            time_str = update_config.get('time', '03:00')

            if frequency == 'biweekly':
                # Schedule for 1st and 15th of each month
                schedule.every().day.at(time_str).do(self.run_analysis_update)
                self.logger.info(f"Scheduled analysis update daily at {time_str}")

        # Full review schedule
        if schedule_config.get('full_review', {}).get('enabled', True):
            review_config = schedule_config['full_review']
            frequency = review_config.get('frequency', 'quarterly')
            time_str = review_config.get('time', '04:00')

            if frequency == 'quarterly':
                # This would need more complex scheduling logic
                # For now, schedule monthly as approximation
                schedule.every(30).days.at(time_str).do(self.run_full_review)
                self.logger.info(f"Scheduled full review every 30 days at {time_str}")

    def run_full_review(self):
        """Run complete review process"""
        self.logger.info("Running full review process...")

        # Run all components in sequence
        self.run_literature_search()

        # Wait a bit between processes
        time.sleep(300)  # 5 minutes

        self.run_data_extraction()

        time.sleep(300)  # 5 minutes

        self.run_analysis_update()

        self.send_notification(
            "Full Review Completed",
            "Complete living review cycle finished successfully"
        )

    def run_continuously(self):
        """Run the scheduler continuously"""
        self.logger.info("Starting living review scheduler...")

        # Setup initial schedule
        self.setup_schedule()

        # Send startup notification
        self.send_notification(
            "Living Review System Started",
            "Automated living review system is now running and monitoring for updates"
        )

        try:
            # Run the scheduler
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")
            self.send_notification(
                "Living Review System Stopped",
                "Automated living review system has been stopped"
            )
        except Exception as e:
            self.logger.error(f"Scheduler error: {e}")
            self.send_notification(
                "Living Review System Error",
                f"Scheduler encountered an error: {e}",
                priority="high"
            )

    def run_once(self, component: str = "all"):
        """Run a single update cycle"""
        self.logger.info(f"Running one-time update: {component}")

        if component == "search" or component == "all":
            self.run_literature_search()

        if component == "extraction" or component == "all":
            self.run_data_extraction()

        if component == "analysis" or component == "all":
            self.run_analysis_update()

        if component == "full":
            self.run_full_review()

        self.logger.info("One-time update completed")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Living Review Scheduler')
    parser.add_argument('--run-once', choices=['search', 'extraction', 'analysis', 'full', 'all'],
                       help='Run a single update cycle')
    parser.add_argument('--continuous', action='store_true',
                       help='Run scheduler continuously')

    args = parser.parse_args()

    scheduler = LivingReviewScheduler()

    if args.run_once:
        scheduler.run_once(args.run_once)
        return 0
    elif args.continuous:
        scheduler.run_continuously()
        return 0
    else:
        # Default to running once
        scheduler.run_once("all")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
