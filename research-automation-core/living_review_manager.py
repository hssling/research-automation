"""
Living Systematic Review Management System
Continuous evidence synthesis and automated review updates
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json
import requests
from datetime import datetime, timedelta
import schedule
import time
import threading
from dataclasses import dataclass, asdict
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ReviewUpdate:
    """Represents a review update event"""
    review_id: str
    update_type: str  # 'new_evidence', 'major_update', 'minor_update'
    trigger_date: str
    new_studies_count: int = 0
    removed_studies_count: int = 0
    effect_change: Optional[float] = None
    heterogeneity_change: Optional[float] = None
    description: str = ""
    risk_assessment: str = ""


@dataclass
class Stakeholder:
    """Represents a stakeholder in the living review"""
    id: str
    email: str
    name: str
    role: str  # 'researcher', 'clinician', 'policymaker', 'patient'
    notification_frequency: str  # 'immediate', 'weekly', 'monthly'
    last_notification: Optional[str] = None
    preferences: Dict[str, Any] = None


class EvidenceMonitor:
    """Monitors new evidence sources continuously"""

    def __init__(self, review_id: str, search_strategy: Dict[str, Any]):
        self.review_id = review_id
        self.search_strategy = search_strategy
        self.last_check = datetime.now()
        self.sources = {
            'pubmed': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
            'cochrane': 'https://www.cochranelibrary.com/api',
            'clinicaltrials': 'https://clinicaltrials.gov/api/v2'
        }

    def check_for_updates(self) -> Dict[str, Any]:
        """Check all sources for new or updated evidence"""

        logger.info(f"Checking for evidence updates for review {self.review_id}")

        updates = {
            'pubmed': self._check_pubmed_updates(),
            'cochrane': self._check_cochrane_updates(),
            'clinicaltrials': self._check_clinical_trials_updates(),
            'timestamp': datetime.now().isoformat()
        }

        # Combine all new studies
        all_new_studies = []
        for source, data in updates.items():
            if isinstance(data, list):
                all_new_studies.extend(data)

        updates['total_new_studies'] = len(all_new_studies)
        updates['new_studies'] = all_new_studies

        logger.info(f"Found {len(all_new_studies)} new studies across all sources")
        return updates

    def _check_pubmed_updates(self) -> List[Dict[str, Any]]:
        """Check PubMed for new studies"""

        try:
            # Mock PubMed API call - replace with actual eutils API
            query = self.search_strategy.get('pubmed_query', '')
            last_check_date = self.last_check.strftime('%Y/%m/%d')

            # Simulated new studies found
            # In real implementation:
            # 1. Use eSearch to find new studies since last_check_date
            # 2. Use eSummary to get article details
            # 3. Use eFetch to get abstracts if needed

            new_studies = [
                {
                    'pmid': 'mock_001',
                    'title': 'New study on treatment efficacy',
                    'abstract': 'Abstract text...',
                    'source': 'pubmed',
                    'publication_date': datetime.now().strftime('%Y-%m-%d'),
                    'relevance_score': np.random.uniform(0.6, 0.9)
                }
            ]

            return new_studies

        except Exception as e:
            logger.error(f"Error checking PubMed: {e}")
            return []

    def _check_cochrane_updates(self) -> List[Dict[str, Any]]:
        """Check Cochrane Library for updates"""

        try:
            # Mock Cochrane API call
            # In real implementation:
            # Use Cochrane's API or scheduled checks for Cochrane Reviews updates

            return []  # Usually fewer updates from Cochrane

        except Exception as e:
            logger.error(f"Error checking Cochrane: {e}")
            return []

    def _check_clinical_trials_updates(self) -> List[Dict[str, Any]]:
        """Check ClinicalTrials.gov for new registered trials"""

        try:
            # Mock ClinicalTrials.gov API call
            # In real implementation:
            # Query ClinicalTrials.gov API for new trials matching inclusion criteria

            new_trials = [
                {
                    'nct_id': 'NCT_mock_001',
                    'title': 'New clinical trial',
                    'condition': 'Study condition',
                    'source': 'clinicaltrials',
                    'registration_date': datetime.now().strftime('%Y-%m-%d')
                }
            ]

            return new_trials

        except Exception as e:
            logger.error(f"Error checking ClinicalTrials.gov: {e}")
            return []


class LivingReviewEngine:
    """Core engine for managing living systematic reviews"""

    def __init__(self, database_path: str = "living_reviews.db"):
        self.db_path = Path(database_path)
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for living reviews"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS living_reviews (
                    review_id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    search_strategy TEXT,
                    last_update TEXT,
                    total_studies INTEGER,
                    included_studies INTEGER,
                    created_date TEXT,
                    update_frequency TEXT,
                    status TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_studies (
                    id INTEGER PRIMARY KEY,
                    review_id TEXT,
                    study_id TEXT,
                    source TEXT,
                    title TEXT,
                    authors TEXT,
                    abstract TEXT,
                    publication_date TEXT,
                    relevance_score REAL,
                    inclusion_status TEXT,
                    added_date TEXT,
                    removed_date TEXT,
                    removal_reason TEXT,
                    FOREIGN KEY (review_id) REFERENCES living_reviews (review_id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_updates (
                    id INTEGER PRIMARY KEY,
                    review_id TEXT,
                    update_type TEXT,
                    trigger_date TEXT,
                    new_studies_count INTEGER,
                    removed_studies_count INTEGER,
                    effect_change REAL,
                    heterogeneity_change REAL,
                    description TEXT,
                    risk_assessment TEXT,
                    processed_date TEXT,
                    FOREIGN KEY (review_id) REFERENCES living_reviews (review_id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stakeholders (
                    id TEXT PRIMARY KEY,
                    review_id TEXT,
                    email TEXT,
                    name TEXT,
                    role TEXT,
                    notification_frequency TEXT,
                    last_notification TEXT,
                    preferences TEXT,
                    FOREIGN KEY (review_id) REFERENCES living_reviews (review_id)
                )
            ''')

            conn.commit()

        logger.info(f"Initialized living reviews database: {self.db_path}")

    def create_living_review(self, review_id: str, title: str, description: str,
                           search_strategy: Dict[str, Any], update_frequency: str = 'weekly') -> bool:
        """Create a new living systematic review"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO living_reviews
                    (review_id, title, description, search_strategy, last_update,
                     total_studies, included_studies, created_date, update_frequency, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    review_id, title, description, json.dumps(search_strategy),
                    datetime.now().isoformat(), 0, 0,
                    datetime.now().isoformat(), update_frequency, 'active'
                ))
                conn.commit()

            logger.info(f"Created living review: {review_id}")
            return True

        except Exception as e:
            logger.error(f"Error creating living review: {e}")
            return False

    def add_stakeholder(self, stakeholder: Stakeholder) -> bool:
        """Add a stakeholder to a living review"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO stakeholders
                    (id, review_id, email, name, role, notification_frequency,
                     last_notification, preferences)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    stakeholder.id, stakeholder.review_id, stakeholder.email,
                    stakeholder.name, stakeholder.role,
                    stakeholder.notification_frequency,
                    stakeholder.last_notification or datetime.now().isoformat(),
                    json.dumps(stakeholder.preferences) if stakeholder.preferences else None
                ))
                conn.commit()

            logger.info(f"Added stakeholder {stakeholder.name} to review {stakeholder.review_id}")
            return True

        except Exception as e:
            logger.error(f"Error adding stakeholder: {e}")
            return False

    def update_review_with_new_evidence(self, review_id: str, new_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update a living review with new evidence"""

        logger.info(f"Updating review {review_id} with {len(new_evidence)} new studies")

        # Screen new studies for inclusion
        potentially_relevant = self._screen_new_studies(new_evidence)
        included_studies = self._assess_inclusion_criteria(review_id, potentially_relevant)

        # Estimate impact on results
        impact = self._assess_update_impact(review_id, included_studies)

        # Create update record
        update = ReviewUpdate(
            review_id=review_id,
            update_type='new_evidence' if included_studies else 'no_change',
            trigger_date=datetime.now().isoformat(),
            new_studies_count=len(included_studies),
            effect_change=impact.get('effect_change'),
            heterogeneity_change=impact.get('heterogeneity_change'),
            description=f"Added {len(included_studies)} new studies to review",
            risk_assessment=impact.get('risk_assessment', 'Low risk')
        )

        # Save update to database
        self._save_update(update)

        # Update study records
        for study in included_studies:
            self._add_study_to_review(review_id, study)

        # Update review metadata
        self._update_review_metadata(review_id, len(included_studies))

        logger.info(f"Review {review_id} updated with {len(included_studies)} new included studies")

        return asdict(update)

    def _screen_new_studies(self, new_studies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Initial screening of new studies"""

        screened = []

        for study in new_studies:
            # Basic relevance check based on title and abstract
            title_abstract = f"{study.get('title', '')} {study.get('abstract', '')}".lower()

            # Simple inclusion criteria (expand with actual logic)
            if any(keyword in title_abstract for keyword in ['treatment', 'intervention', 'study']):
                study['screening_status'] = 'potentially_relevant'
                screened.append(study)

        logger.info(f"Initial screening: {len(screened)}/{len(new_studies)} studies potentially relevant")
        return screened

    def _assess_inclusion_criteria(self, review_id: str, candidate_studies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assess inclusion criteria for candidate studies"""

        # For now, use a simple inclusion rule
        # In practice, this would integrate with the existing AI screening system

        included = []
        for study in candidate_studies:
            relevance_score = study.get('relevance_score', 0.5)

            # Arbitrary threshold - replace with ML model
            if relevance_score > 0.7:
                study['inclusion_status'] = 'included'
                study['inclusion_date'] = datetime.now().isoformat()
                included.append(study)
            else:
                study['inclusion_status'] = 'excluded'
                study['exclusion_reason'] = 'Low relevance score'

        logger.info(f"Inclusion assessment: {len(included)}/{len(candidate_studies)} studies included")
        return included

    def _assess_update_impact(self, review_id: str, new_studies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess the impact of new studies on review results"""

        return {
            'effect_change': None,  # Would calculate actual effect change
            'heterogeneity_change': None,  # Would assess heterogeneity impact
            'risk_assessment': 'Low risk - minor update'
        }

    def _save_update(self, update: ReviewUpdate):
        """Save update to database"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO review_updates
                (review_id, update_type, trigger_date, new_studies_count,
                 removed_studies_count, effect_change, heterogeneity_change,
                 description, risk_assessment, processed_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                update.review_id, update.update_type, update.trigger_date,
                update.new_studies_count, update.removed_studies_count,
                update.effect_change, update.heterogeneity_change,
                update.description, update.risk_assessment,
                datetime.now().isoformat()
            ))
            conn.commit()

    def _add_study_to_review(self, review_id: str, study: Dict[str, Any]):
        """Add a study to the review database"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO review_studies
                (review_id, study_id, source, title, authors, abstract,
                 publication_date, relevance_score, inclusion_status, added_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                review_id, study.get('study_id', study.get('pmid', 'unknown')),
                study.get('source'), study.get('title'), study.get('authors'),
                study.get('abstract'), study.get('publication_date'),
                study.get('relevance_score', 0.5), study.get('inclusion_status'),
                datetime.now().isoformat()
            ))
            conn.commit()

    def _update_review_metadata(self, review_id: str, new_studies_count: int):
        """Update review metadata after adding studies"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE living_reviews
                SET last_update = ?, total_studies = total_studies + ?, included_studies = included_studies + ?
                WHERE review_id = ?
            ''', (
                datetime.now().isoformat(),
                new_studies_count, new_studies_count,
                review_id
            ))
            conn.commit()

    def get_review_status(self, review_id: str) -> Dict[str, Any]:
        """Get current status of a living review"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM living_reviews WHERE review_id = ?
            ''', (review_id,))

            row = cursor.fetchone()
            if not row:
                return None

            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))


class NotificationSystem:
    """Handles notifications and stakeholder communication"""

    def __init__(self, smtp_config: Dict[str, str] = None):
        self.smtp_config = smtp_config or {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': 'your-email@example.com',
            'password': 'your-password'
        }

    def send_update_notification(self, stakeholder: Stakeholder, update: ReviewUpdate) -> bool:
        """Send update notification to stakeholder"""

        logger.info(f"Sending notification to {stakeholder.email}")

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = stakeholder.email
            msg['Subject'] = f"Living Review Update: {update.review_id}"

            body = self._create_notification_body(update, stakeholder)
            msg.attach(MIMEText(body, 'html'))

            # In real implementation, connect and send
            # For demo, just log
            logger.info(f"Would send email to {stakeholder.email} about update {update.update_type}")

            # Update last notification time
            stakeholder.last_notification = datetime.now().isoformat()

            return True

        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return False

    def _create_notification_body(self, update: ReviewUpdate, stakeholder: Stakeholder) -> str:
        """Create HTML notification message"""

        html = f"""
<h2>Review Update Notification</h2>

<p>Dear {stakeholder.name},</p>

<p>A {update.update_type.replace('_', ' ')} has been made to the living systematic review "{update.review_id}".</p>

<div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
<h3>Update Summary</h3>
<ul>
<li><strong>Type:</strong> {update.update_type.replace('_', ' ').title()}</li>
<li><strong>Date:</strong> {update.trigger_date[:10]}</li>
<li><strong>New Studies Added:</strong> {update.new_studies_count}</li>
<li><strong>Risk Assessment:</strong> {update.risk_assessment}</li>
</ul>
{ f"<p><strong>Description:</strong> {update.description}</p>" if update.description else "" }
</div>

<h3>Risk Assessment</h3>
<p>{update.risk_assessment}</p>

"""

        if stakeholder.role == 'clinician':
            html += """
<p><strong>For Clinicians:</strong> This update may affect clinical practice guidelines.
Please review the updated evidence before making treatment decisions.</p>
"""
        elif stakeholder.role == 'policymaker':
            html += """
<p><strong>For Policymakers:</strong> This update may influence health policy recommendations.
The policy team has been notified for consideration in upcoming reviews.</p>
"""

        html += """

<p>If you have questions about this update, please contact the review team.</p>

<p>Best regards,<br>The Living Review Management System</p>

<hr style="margin: 30px 0;">
<p style="font-size: small; color: #666;">
This notification was sent because you are subscribed to updates for this review.
To change your notification preferences, contact the system administrator.
</p>

"""

        return html


class LivingReviewScheduler:
    """Handles scheduling and automated execution of living review updates"""

    def __init__(self):
        self.is_running = False
        self.thread = None
        self.review_engine = None

    def start_automated_updates(self, engine: LivingReviewEngine):
        """Start automated review update schedule"""

        self.review_engine = engine
        self.is_running = True

        def run_scheduler():
            while self.is_running:
                # Schedule updates (simplified - in real implementation use proper scheduling)
                # Check for updates every 5 minutes for demo
                time.sleep(300)  # 5 minutes

                if not self.is_running:
                    break

                # Find reviews due for update
                reviews_to_update = self._get_due_reviews()

                for review_id in reviews_to_update:
                    logger.info(f"Processing scheduled update for review {review_id}")
                    self._process_review_update(review_id)

        self.thread = threading.Thread(target=run_scheduler, daemon=True)
        self.thread.start()

        logger.info("Started automated living review updates")

    def stop_automated_updates(self):
        """Stop automated review updates"""

        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)

        logger.info("Stopped automated living review updates")

    def _get_due_reviews(self) -> List[str]:
        """Get reviews due for update"""

        # Simplified - in reality check frequency and last update time
        with sqlite3.connect(self.review_engine.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT review_id FROM living_reviews
                WHERE status = 'active'
                LIMIT 5  -- Check first 5 active reviews
            ''')

            return [row[0] for row in cursor.fetchall()]

    def _process_review_update(self, review_id: str):
        """Process a review update"""

        try:
            # Get review search strategy
            review_status = self.review_engine.get_review_status(review_id)
            if not review_status:
                logger.warning(f"Review {review_id} not found")
                return

            search_strategy = json.loads(review_status['search_strategy'])

            # Create evidence monitor and check for updates
            monitor = EvidenceMonitor(review_id, search_strategy)
            updates = monitor.check_for_updates()

            if updates['total_new_studies'] > 0:
                # Process the update
                update_result = self.review_engine.update_review_with_new_evidence(
                    review_id, updates['new_studies']
                )

                logger.info(f"Processed update for review {review_id}: {update_result}")
            else:
                logger.info(f"No new evidence found for review {review_id}")

        except Exception as e:
            logger.error(f"Error processing update for review {review_id}: {e}")


# Main Living Review Manager
class LivingReviewManager:
    """Main interface for managing living systematic reviews"""

    def __init__(self, database_path: str = "living_reviews.db"):
        self.engine = LivingReviewEngine(database_path)
        self.evidence_monitor = None
        self.scheduler = LivingReviewScheduler()
        self.notifier = NotificationSystem()

    def create_review_and_monitor(self, review_id: str, title: str, description: str,
                                search_strategy: Dict[str, Any], stakeholders: List[Stakeholder] = None) -> bool:
        """Create a living review with monitoring setup"""

        # Create the review
        if not self.engine.create_living_review(review_id, title, description, search_strategy):
            return False

        # Add stakeholders
        stakeholders = stakeholders or []
        for stakeholder in stakeholders:
            stakeholder.review_id = review_id
            self.engine.add_stakeholder(stakeholder)

        # Setup evidence monitor
        self.evidence_monitor = EvidenceMonitor(review_id, search_strategy)

        logger.info(f"Successfully created living review {review_id} with monitoring")
        return True

    def perform_manual_update(self, review_id: str) -> Dict[str, Any]:
        """Manually trigger an update check for a review"""

        if not self.evidence_monitor:
            # Reinitialize for the review
            review_status = self.engine.get_review_status(review_id)
            if review_status:
                search_strategy = json.loads(review_status['search_strategy'])
                self.evidence_monitor = EvidenceMonitor(review_id, search_strategy)
            else:
                raise ValueError(f"Review {review_id} not found")

        # Check for updates
        updates = self.evidence_monitor.check_for_updates()

        # Process updates if found
        if updates['total_new_studies'] > 0:
            update_result = self.engine.update_review_with_new_evidence(
                review_id, updates['new_studies']
            )

            # Send notifications
            self._send_update_notifications(review_id, update_result)

            return {
                'update_performed': True,
                'updates_found': len(updates['new_studies']),
                'result': update_result
            }
        else:
            return {
                'update_performed': False,
                'updates_found': 0,
                'message': 'No new evidence found'
            }

    def _send_update_notifications(self, review_id: str, update_result: Dict[str, Any]):
        """Send notifications to stakeholders about the update"""

        try:
            # Get stakeholders for this review
            stakeholders = self._get_stakeholders(review_id)

            update = ReviewUpdate(**update_result)

            for stakeholder_dict in stakeholders:
                stakeholder = Stakeholder(
                    id=stakeholder_dict['id'],
                    review_id=stakeholder_dict['review_id'],
                    email=stakeholder_dict['email'],
                    name=stakeholder_dict['name'],
                    role=stakeholder_dict['role'],
                    notification_frequency=stakeholder_dict['notification_frequency'],
                    last_notification=stakeholder_dict.get('last_notification'),
                    preferences=json.loads(stakeholder_dict['preferences']) if stakeholder_dict['preferences'] else None
                )

                self.notifier.send_update_notification(stakeholder, update)

        except Exception as e:
            logger.error(f"Error sending notifications: {e}")

    def _get_stakeholders(self, review_id: str) -> List[Dict[str, Any]]:
        """Get stakeholders for a review"""

        with sqlite3.connect(self.engine.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM stakeholders WHERE review_id = ?', (review_id,))
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def start_automated_monitoring(self):
        """Start automated monitoring for all living reviews"""

        self.scheduler.start_automated_updates(self.engine)
        logger.info("Started automated monitoring for all living reviews")

    def stop_automated_monitoring(self):
        """Stop automated monitoring"""

        self.scheduler.stop_automated_updates()
        logger.info("Stopped automated monitoring")

    def get_review_report(self, review_id: str) -> Dict[str, Any]:
        """Generate a comprehensive report for a living review"""

        review_status = self.engine.get_review_status(review_id)
        if not review_status:
            return {"error": f"Review {review_id} not found"}

        # Get study counts
        with sqlite3.connect(self.engine.db_path) as conn:
            cursor = conn.cursor()

            # Count studies by status
            cursor.execute('''
                SELECT inclusion_status, COUNT(*) as count
                FROM review_studies
                WHERE review_id = ?
                GROUP BY inclusion_status
            ''', (review_id,))

            study_counts = dict(cursor.fetchall())

        # Get recent updates
        with sqlite3.connect(self.engine.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT update_type, trigger_date, new_studies_count
                FROM review_updates
                WHERE review_id = ?
                ORDER BY trigger_date DESC
                LIMIT 10
            ''', (review_id,))

            recent_updates = cursor.fetchall()

        return {
            'review_info': review_status,
            'study_counts': study_counts,
            'recent_updates': recent_updates,
            'total_studies': review_status.get('total_studies', 0),
            'included_studies': review_status.get('included_studies', 0),
            'last_update': review_status.get('last_update', 'Never')
        }


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Living Systematic Review Manager")
    parser.add_argument("command", choices=['create', 'update', 'status', 'start-monitoring', 'stop-monitoring'],
                       help="Command to execute")
    parser.add_argument("--review-id", help="Review ID for operations")
    parser.add_argument("--title", help="Review title")
    parser.add_argument("--description", help="Review description")
    parser.add_argument("--search-strategy", help="Search strategy JSON file")

    args = parser.parse_args()

    # Initialize manager
    manager = LivingReviewManager()

    if args.command == 'create':
        if not args.review_id or not args.title or not args.search_strategy:
            parser.error("--review-id, --title, and --search-strategy required for create")

        # Load search strategy
        with open(args.search_strategy, 'r') as f:
            search_strategy = json.load(f)

        # Create review
        manager.create_review_and_monitor(args.review_id, args.title,
                                       args.description or "", search_strategy)

        print(f"Created living review: {args.review_id}")

    elif args.command == 'update':
        if not args.review_id:
            parser.error("--review-id required for update")

        result = manager.perform_manual_update(args.review_id)
        print("Update completed successfully!")
        print(f"Updates found: {result.get('updates_found', 0)}")

    elif args.command == 'status':
        if not args.review_id:
            parser.error("--review-id required for status")

        report = manager.get_review_report(args.review_id)
        if 'error' in report:
            print(f"Error: {report['error']}")
        else:
            print(f"Review: {args.review_id}")
            print(f"Total Studies: {report.get('total_studies', 0)}")
            print(f"Included Studies: {report.get('included_studies', 0)}")
            print(f"Last Update: {report.get('last_update', 'Never')}")

    elif args.command == 'start-monitoring':
        manager.start_automated_monitoring()
        print("Started automated monitoring")

    elif args.command == 'stop-monitoring':
        manager.stop_automated_monitoring()
        print("Stopped automated monitoring")
