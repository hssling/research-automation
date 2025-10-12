"""
Global Research Collaboration Platform
Secure federated research networks and multi-institutional collaboration tools
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import re
from dataclasses import dataclass, asdict
import time
import threading
import hashlib
import secrets
import sqlite3
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ResearchInstitution:
    """Represents a research institution in the network"""
    id: str
    name: str
    country: str
    type: str  # 'university', 'hospital', 'government', 'industry', 'nonprofit'
    expertise_areas: List[str]
    resources_available: List[str]  # 'data', 'computing', 'expertise'
    contact_email: str
    public_key: Optional[str] = None
    verified_at: Optional[str] = None
    reputation_score: float = 0.0


@dataclass
class CollaborationProject:
    """Represents a multi-institutional research collaboration"""
    id: str
    title: str
    description: str
    lead_institution: str
    collaborating_institutions: List[str]
    research_question: str
    methodology: str
    data_access_policy: str
    publication_policy: str
    status: str  # 'planning', 'active', 'data_collection', 'analysis', 'writing', 'completed'
    created_at: str
    coordinator_email: str
    privacy_level: str  # 'public', 'restricted', 'confidential'
    milestones: List[Dict[str, Any]] = None


@dataclass
class FederatedQuery:
    """Represents a federated research query across institutions"""
    id: str
    query: str
    requested_by: str
    approved_institutions: List[str]
    rejection_reasons: Dict[str, str]
    privacy_preservation: str
    expected_results_format: str
    deadline: str
    status: str  # 'pending', 'approved', 'partially_approved', 'rejected'
    results_available: bool = False


@dataclass
class SecureDataEnvelope:
    """Represents a secure data sharing envelope"""
    id: str
    project_id: str
    sender_institution: str
    recipient_institutions: List[str]
    data_type: str  # 'aggregated_stats', 'anonymized_records', 'meta_analysis'
    encryption_key: str
    access_policy: str
    expires_at: str
    created_at: str


class InstitutionalRegistry:
    """Manages the global registry of research institutions"""

    def __init__(self, database_path: str = "institutional_registry.db"):
        self.db_path = Path(database_path)
        self._init_database()
        self._generate_keypair()

    def _init_database(self):
        """Initialize institutional registry database"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create institutions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS institutions (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    country TEXT,
                    type TEXT,
                    expertise_areas TEXT,
                    resources_available TEXT,
                    contact_email TEXT,
                    public_key TEXT,
                    verified_at TEXT,
                    reputation_score REAL,
                    created_at TEXT
                )
            ''')

            # Create institution partnerships table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS partnerships (
                    id TEXT PRIMARY KEY,
                    institution_a TEXT,
                    institution_b TEXT,
                    relationship_type TEXT,
                    trust_level TEXT,
                    last_collaboration TEXT,
                    created_at TEXT,
                    FOREIGN KEY (institution_a) REFERENCES institutions (id),
                    FOREIGN KEY (institution_b) REFERENCES institutions (id)
                )
            ''')

            conn.commit()

    def _generate_keypair(self):
        """Generate RSA keypair for secure communications"""
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # Generate public key
            public_key = private_key.public_key()

            # Serialize keys
            self.private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            self.public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            logger.info("Generated secure keypair for federation")

        except Exception as e:
            logger.error(f"Failed to generate keypair: {e}")
            self.private_key_pem = None
            self.public_key_pem = None

    def register_institution(self, institution: ResearchInstitution) -> bool:
        """Register a new research institution"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO institutions
                    (id, name, country, type, expertise_areas, resources_available, contact_email,
                     public_key, verified_at, reputation_score, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    institution.id, institution.name, institution.country, institution.type,
                    ','.join(institution.expertise_areas),
                    ','.join(institution.resources_available),
                    institution.contact_email,
                    institution.public_key or self.public_key_pem.decode(),
                    institution.verified_at or datetime.now().isoformat(),
                    institution.reputation_score, datetime.now().isoformat()
                ))
                conn.commit()

            logger.info(f"Registered institution: {institution.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to register institution: {e}")
            return False

    def find_collaboration_partners(self, institution_id: str, expertise_needed: List[str],
                                  min_reputation: float = 0.0) -> List[ResearchInstitution]:
        """Find potential collaboration partners"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM institutions
                    WHERE id != ? AND reputation_score >= ?
                    ORDER BY reputation_score DESC
                ''', (institution_id, min_reputation))

                institutions = []
                for row in cursor.fetchall():
                    inst_expertise = row[4].split(',') if row[4] else []

                    # Check if institution has needed expertise
                    if any(exp in inst_expertise for exp in expertise_needed):
                        institution = ResearchInstitution(
                            id=row[0], name=row[1], country=row[2], type=row[3],
                            expertise_areas=inst_expertise,
                            resources_available=row[5].split(',') if row[5] else [],
                            contact_email=row[6], public_key=row[7], verified_at=row[8],
                            reputation_score=row[9]
                        )
                        institutions.append(institution)

                return institutions[:10]  # Return top 10 matches

        except Exception as e:
            logger.error(f"Error finding partners: {e}")
            return []

    def update_reputation_score(self, institution_id: str, new_score: float):
        """Update institution reputation score based on collaboration success"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE institutions SET reputation_score = ? WHERE id = ?
                ''', (new_score, institution_id))
                conn.commit()

            logger.info(f"Updated reputation for {institution_id}: {new_score}")

        except Exception as e:
            logger.error(f"Failed to update reputation: {e}")


class CollaborationManager:
    """Manages multi-institutional research collaborations"""

    def __init__(self, database_path: str = "collaborations.db"):
        self.db_path = Path(database_path)
        self._init_database()

    def _init_database(self):
        """Initialize collaborations database"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create projects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    lead_institution TEXT,
                    collaborating_institutions TEXT,
                    research_question TEXT,
                    methodology TEXT,
                    data_access_policy TEXT,
                    publication_policy TEXT,
                    status TEXT,
                    created_at TEXT,
                    coordinator_email TEXT,
                    privacy_level TEXT,
                    milestones TEXT
                )
            ''')

            # Create invitations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invitations (
                    id TEXT PRIMARY KEY,
                    project_id TEXT,
                    recipient_institution TEXT,
                    sender_institution TEXT,
                    message TEXT,
                    status TEXT,
                    sent_at TEXT,
                    responded_at TEXT,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')

            conn.commit()

    def create_collaboration_project(self, project: CollaborationProject) -> bool:
        """Create a new collaboration project"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO projects
                    (id, title, description, lead_institution, collaborating_institutions, research_question,
                     methodology, data_access_policy, publication_policy, status, created_at, coordinator_email,
                     privacy_level, milestones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    project.id, project.title, project.description, project.lead_institution,
                    ','.join(project.collaborating_institutions), project.research_question,
                    project.methodology, project.data_access_policy, project.publication_policy,
                    project.status, project.created_at, project.coordinator_email,
                    project.privacy_level,
                    json.dumps(project.milestones) if project.milestones else None
                ))
                conn.commit()

            logger.info(f"Created collaboration project: {project.title}")
            return True

        except Exception as e:
            logger.error(f"Failed to create project: {e}")
            return False

    def send_collaboration_invitation(self, project_id: str, recipient_institution: str,
                                    sender_institution: str, message: str) -> str:
        """Send collaboration invitation to an institution"""

        invitation_id = secrets.token_urlsafe(32)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO invitations
                    (id, project_id, recipient_institution, sender_institution, message, status, sent_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    invitation_id, project_id, recipient_institution, sender_institution,
                    message, 'pending', datetime.now().isoformat()
                ))
                conn.commit()

            logger.info(f"Sent invitation {invitation_id} to {recipient_institution}")
            return invitation_id

        except Exception as e:
            logger.error(f"Failed to send invitation: {e}")
            return None

    def respond_to_invitation(self, invitation_id: str, response: str,
                            response_message: str = "") -> bool:
        """Respond to a collaboration invitation"""

        try:
            status = 'accepted' if response.lower() == 'accept' else 'declined'

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE invitations SET status = ?, responded_at = ?
                    WHERE id = ?
                ''', (status, datetime.now().isoformat(), invitation_id))
                conn.commit()

            logger.info(f"Invitation {invitation_id} {status}")
            return True

        except Exception as e:
            logger.error(f"Failed to respond to invitation: {e}")
            return False

    def get_project_invitations(self, institution_id: str) -> List[Dict[str, Any]]:
        """Get pending invitations for an institution"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT i.*, p.title, p.description
                    FROM invitations i
                    JOIN projects p ON i.project_id = p.id
                    WHERE i.recipient_institution = ? AND i.status = 'pending'
                    ORDER BY i.sent_at DESC
                ''', (institution_id,))

                invitations = []
                for row in cursor.fetchall():
                    invitation = {
                        'invitation_id': row[0],
                        'project_id': row[1],
                        'recipient': row[2],
                        'sender': row[3],
                        'message': row[4],
                        'status': row[5],
                        'sent_at': row[6],
                        'responded_at': row[7],
                        'project_title': row[8],
                        'project_description': row[9]
                    }
                    invitations.append(invitation)

                return invitations

        except Exception as e:
            logger.error(f"Failed to get invitations: {e}")
            return []


class FederatedQueryEngine:
    """Manages federated research queries across institutions"""

    def __init__(self, registry: InstitutionalRegistry, database_path: str = "federated_queries.db"):
        self.registry = registry
        self.db_path = Path(database_path)
        self._init_database()

    def _init_database(self):
        """Initialize federated queries database"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create queries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS queries (
                    id TEXT PRIMARY KEY,
                    query TEXT,
                    requested_by TEXT,
                    approved_institutions TEXT,
                    rejection_reasons TEXT,
                    privacy_preservation TEXT,
                    expected_results_format TEXT,
                    deadline TEXT,
                    status TEXT,
                    results_available BOOLEAN,
                    created_at TEXT
                )
            ''')

            conn.commit()

    def submit_federated_query(self, query: FederatedQuery) -> bool:
        """Submit a federated query for approval across institutions"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO queries
                    (id, query, requested_by, approved_institutions, rejection_reasons, privacy_preservation,
                     expected_results_format, deadline, status, results_available, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    query.id, query.query, query.requested_by,
                    ','.join(query.approved_institutions) if query.approved_institutions else '',
                    json.dumps(query.rejection_reasons) if query.rejection_reasons else '{}',
                    query.privacy_preservation, query.expected_results_format,
                    query.deadline, query.status, query.results_available,
                    datetime.now().isoformat()
                ))
                conn.commit()

            logger.info(f"Submitted federated query: {query.id}")
            return True

        except Exception as e:
            logger.error(f"Failed to submit query: {e}")
            return False

    def approve_query_institution(self, query_id: str, institution_id: str) -> bool:
        """Approve a federated query for an institution"""

        try:
            # Get current approvals
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT approved_institutions FROM queries WHERE id = ?', (query_id,))
                row = cursor.fetchone()

                if row and row[0]:
                    approved = row[0].split(',')
                    if institution_id not in approved:
                        approved.append(institution_id)

                        cursor.execute('''
                            UPDATE queries SET approved_institutions = ? WHERE id = ?
                        ''', (','.join(approved), query_id))
                        conn.commit()

                        # Check if we have sufficient approvals to proceed
                        self._check_query_threshold(query_id)

                        logger.info(f"Institution {institution_id} approved query {query_id}")
                        return True

            return False

        except Exception as e:
            logger.error(f"Failed to approve query: {e}")
            return False

    def reject_query_institution(self, query_id: str, institution_id: str, reason: str) -> bool:
        """Reject a federated query for an institution"""

        try:
            # Get current rejection reasons
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT rejection_reasons FROM queries WHERE id = ?', (query_id,))
                row = cursor.fetchone()

                if row and row[0]:
                    reasons = json.loads(row[0])
                    reasons[institution_id] = reason

                    cursor.execute('''
                        UPDATE queries SET rejection_reasons = ? WHERE id = ?
                    ''', (json.dumps(reasons), query_id))
                    conn.commit()

                    logger.info(f"Institution {institution_id} rejected query {query_id}: {reason}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Failed to reject query: {e}")
            return False

    def _check_query_threshold(self, query_id: str):
        """Check if query has reached approval threshold to proceed"""

        try:
            # Get all institutions that could potentially participate
            # This is a simplified version - in real implementation would query registry
            potential_institutions = self._get_potential_institutions(query_id)

            approved_count = len(self._get_approved_institutions(query_id))

            # Require at least 3 approvals or 30% of potential institutions
            threshold = min(3, max(1, int(len(potential_institutions) * 0.3)))

            if approved_count >= threshold:
                self._update_query_status(query_id, 'approved')
                logger.info(f"Query {query_id} reached approval threshold ({approved_count}/{threshold})")

        except Exception as e:
            logger.error(f"Error checking threshold: {e}")

    def _get_potential_institutions(self, query_id: str) -> List[str]:
        """Get list of institutions that could participate in query"""
        # Simplified - would integrate with registry to find relevant institutions
        return ['inst_001', 'inst_002', 'inst_003', 'inst_004', 'inst_005']

    def _get_approved_institutions(self, query_id: str) -> List[str]:
        """Get list of institutions that approved the query"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT approved_institutions FROM queries WHERE id = ?', (query_id,))
                row = cursor.fetchone()

                if row and row[0]:
                    return row[0].split(',')
                return []

        except Exception as e:
            logger.error(f"Error getting approved institutions: {e}")
            return []

    def _update_query_status(self, query_id: str, status: str):
        """Update query status"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE queries SET status = ? WHERE id = ?', (status, query_id))
                conn.commit()

        except Exception as e:
            logger.error(f"Failed to update status: {e}")


class SecureDataSharing:
    """Manages secure data sharing across institutions"""

    def __init__(self, registry: InstitutionalRegistry, database_path: str = "secure_sharing.db"):
        self.registry = registry
        self.db_path = Path(database_path)
        self._init_database()

    def _init_database(self):
        """Initialize secure data sharing database"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create data envelopes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_envelopes (
                    id TEXT PRIMARY KEY,
                    project_id TEXT,
                    sender_institution TEXT,
                    recipient_institutions TEXT,
                    data_type TEXT,
                    encryption_key TEXT,
                    access_policy TEXT,
                    expires_at TEXT,
                    created_at TEXT,
                    status TEXT
                )
            ''')

            # Create access logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY,
                    envelope_id TEXT,
                    accessor_institution TEXT,
                    access_type TEXT,
                    access_time TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (envelope_id) REFERENCES data_envelopes (id)
                )
            ''')

            conn.commit()

    def create_secure_envelope(self, envelope: SecureDataEnvelope) -> bool:
        """Create a secure data sharing envelope"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO data_envelopes
                    (id, project_id, sender_institution, recipient_institutions, data_type,
                     encryption_key, access_policy, expires_at, created_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    envelope.id, envelope.project_id, envelope.sender_institution,
                    ','.join(envelope.recipient_institutions), envelope.data_type,
                    envelope.encryption_key, envelope.access_policy,
                    envelope.expires_at, envelope.created_at, 'active'
                ))
                conn.commit()

            logger.info(f"Created secure envelope: {envelope.id}")
            return True

        except Exception as e:
            logger.error(f"Failed to create envelope: {e}")
            return False

    def log_data_access(self, envelope_id: str, institution_id: str, access_type: str,
                       ip_address: str = "", user_agent: str = "") -> bool:
        """Log data access for audit purposes"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO access_logs
                    (envelope_id, accessor_institution, access_type, access_time, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    envelope_id, institution_id, access_type,
                    datetime.now().isoformat(), ip_address, user_agent
                ))
                conn.commit()

            logger.info(f"Logged access to envelope {envelope_id} by {institution_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to log access: {e}")
            return False

    def verify_data_access(self, envelope_id: str, requesting_institution: str) -> bool:
        """Verify if institution has access to envelope"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT recipient_institutions, expires_at, status
                    FROM data_envelopes WHERE id = ?
                ''', (envelope_id,))

                row = cursor.fetchone()
                if not row:
                    return False

                recipients = row[0].split(',')
                expires_at = row[1]
                status = row[2]

                # Check if envelope is active and not expired
                if status != 'active':
                    return False

                if datetime.fromisoformat(expires_at) < datetime.now():
                    # Mark as expired
                    cursor.execute("UPDATE data_envelopes SET status = 'expired' WHERE id = ?",
                                 (envelope_id,))
                    conn.commit()
                    return False

                # Check if requesting institution is authorized
                return requesting_institution in recipients

        except Exception as e:
            logger.error(f"Error verifying access: {e}")
            return False


class GlobalCollaborationPlatform:
    """Main interface for the global research collaboration platform"""

    def __init__(self):
        self.registry = InstitutionalRegistry()
        self.collaboration_manager = CollaborationManager()
        self.query_engine = FederatedQueryEngine(self.registry)
        self.data_sharing = SecureDataSharing(self.registry)

    def onboard_institution(self, institution: ResearchInstitution) -> bool:
        """Onboard a new institution to the collaboration platform"""

        success = self.registry.register_institution(institution)

        if success:
            # Create welcome materials (simplified)
            logger.info(f"Successfully onboarded {institution.name}")
            self._send_welcome_notification(institution)

        return success

    def _send_welcome_notification(self, institution: ResearchInstitution):
        """Send welcome notification to new institution"""
        # This would integrate with email system
        logger.info(f"Welcome notification sent to {institution.contact_email}")

    def initiate_collaboration(self, project: CollaborationProject) -> str:
        """Initiate a new multi-institutional research collaboration"""

        # Generate unique project ID
        project.id = f"project_{secrets.token_urlsafe(16)}"
        project.created_at = datetime.now().isoformat()

        # Validate lead institution exists
        lead_institution = self.registry.get_institution(project.lead_institution)
        if not lead_institution:
            raise ValueError(f"Lead institution {project.lead_institution} not registered")

        success = self.collaboration_manager.create_collaboration_project(project)

        if success:
            # Send invitations to collaborating institutions
            for institution_id in project.collaborating_institutions:
                recipient = self.registry.get_institution(institution_id)
                if recipient:
                    message = f"""
                    You've been invited to collaborate on the project: {project.title}

                    Project Description: {project.description}
                    Research Question: {project.research_question}
                    Coordinator: {project.coordinator_email}

                    Privacy Level: {project.privacy_level}
                    Data Access Policy: {project.data_access_policy}

                    Please review the collaboration terms and respond.
                    """

                    invitation_id = self.collaboration_manager.send_collaboration_invitation(
                        project.id, institution_id, project.lead_institution, message
                    )

                    logger.info(f"Sent collaboration invitation {invitation_id} to {institution_id}")

            return project.id

        return None

    def submit_federated_research_query(self, query_statement: str, requester_institution: str,
                                       privacy_level: str = 'differential_privacy') -> str:
        """Submit a federated research query across multiple institutions"""

        # Generate query ID
        query_id = f"fed_query_{secrets.token_urlsafe(16)}"

        # Determine which institutions to query based on expertise
        target_institutions = self.registry.find_collaboration_partners(
            requester_institution, ['meta-analysis', 'epidemiology'], 0.7
        )

        if not target_institutions:
            raise ValueError("No suitable institutions found for federated query")

        federated_query = FederatedQuery(
            id=query_id,
            query=query_statement,
            requested_by=requester_institution,
            approved_institutions=[],  # Will be populated as approvals come in
            rejection_reasons={},
            privacy_preservation=privacy_level,
            expected_results_format='aggregated_statistics',
            deadline=(datetime.now() + timedelta(days=30)).isoformat(),
            status='pending'
        )

        success = self.query_engine.submit_federated_query(federated_query)

        if success:
            # Send query requests to target institutions
            for institution in target_institutions[:5]:  # Limit to 5 for initial testing
                self._send_query_request(institution.id, federated_query)

            return query_id

        return None

    def _send_query_request(self, institution_id: str, query: FederatedQuery):
        """Send federated query request to institution"""
        # This would integrate with notification system
        logger.info(f"Query request {query.id} sent to {institution_id}")

    def get_institution(self, institution_id: str) -> Optional[ResearchInstitution]:
        """Get institution information from registry"""

        try:
            with sqlite3.connect(self.registry.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM institutions WHERE id = ?', (institution_id,))
                row = cursor.fetchone()

                if row:
                    return ResearchInstitution(
                        id=row[0], name=row[1], country=row[2], type=row[3],
                        expertise_areas=row[4].split(',') if row[4] else [],
                        resources_available=row[5].split(',') if row[5] else [],
                        contact_email=row[6], public_key=row[7], verified_at=row[8],
                        reputation_score=row[9]
                    )

        except Exception as e:
            logger.error(f"Error getting institution: {e}")

        return None

    def get_platform_stats(self) -> Dict[str, Any]:
        """Get global collaboration platform statistics"""

        try:
            # Count institutions
            with sqlite3.connect(self.registry.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM institutions')
                institution_count = cursor.fetchone()[0]

            # Count active collaborations
            with sqlite3.connect(self.collaboration_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM projects WHERE status IN ('active', 'data_collection', 'analysis', 'writing')")
                active_projects = cursor.fetchone()[0]

            # Count federated queries
            with sqlite3.connect(self.query_engine.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM queries')
                query_count = cursor.fetchone()[0]

            return {
                'registered_institutions': institution_count,
                'active_collaborations': active_projects,
                'federated_queries_submitted': query_count,
                'data_sharing_envelopes': 0,  # Would count from data_sharing.db
                'generated_at': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting platform stats: {e}")
            return {}


# CLI Interface
def main():
    """Command line interface for the Global Collaboration Platform"""

    parser = argparse.ArgumentParser(description="Global Research Collaboration Platform")
    parser.add_argument("command", choices=['onboard', 'create-project', 'submit-query', 'stats', 'list-partners'])
    parser.add_argument("--institution-id", help="Institution identifier")
    parser.add_argument("--name", help="Institution or project name")
    parser.add_argument("--query", help="Federated query statement")
    parser.add_argument("--config", help="Configuration JSON file")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    platform = GlobalCollaborationPlatform()

    if args.command == 'onboard' and args.config:
        # Load institution config from JSON
        with open(args.config, 'r') as f:
            config = json.load(f)

        institution = ResearchInstitution(
            id=args.institution_id or config['id'],
            name=config['name'],
            country=config['country'],
            type=config['type'],
            expertise_areas=config.get('expertise_areas', []),
            resources_available=config.get('resources_available', []),
            contact_email=config['contact_email']
        )

        success = platform.onboard_institution(institution)
        print(f"Institution {'onboarded' if success else 'onboarding failed'}")

    elif args.command == 'create-project' and args.config:
        # Load project config from JSON
        with open(args.config, 'r') as f:
            config = json.load(f)

        project = CollaborationProject(
            id="",  # Will be generated
            title=config['title'],
            description=config['description'],
            lead_institution=args.institution_id,
            collaborating_institutions=config.get('collaborators', []),
            research_question=config['research_question'],
            methodology=config['methodology'],
            data_access_policy=config.get('data_policy', 'restricted'),
            publication_policy=config.get('publication_policy', 'open_access'),
            status='planning',
            created_at="",  # Will be set
            coordinator_email=config['coordinator_email'],
            privacy_level=config.get('privacy_level', 'restricted')
        )

        project_id = platform.initiate_collaboration(project)
        print(f"Project created: {project_id}" if project_id else "Project creation failed")

    elif args.command == 'submit-query' and args.query and args.institution_id:
        query_id = platform.submit_federated_research_query(args.query, args.institution_id)
        print(f"Federated query submitted: {query_id}" if query_id else "Query submission failed")

    elif args.command == 'stats':
        stats = platform.get_platform_stats()
        print("Global Collaboration Platform Statistics:")
        for key, value in stats.items():
            if key != 'generated_at':
                print(f"  {key}: {value}")

    elif args.command == 'list-partners' and args.institution_id:
        # This would require additional configuration for expertise areas
        print("Partner discovery requires expertise specification")
        print("Use --config to provide institution profile")


if __name__ == "__main__":
    import sys
    main()


print("Global Research Collaboration Platform initialized")
print("Ready for multi-institutional federated research collaborations")
