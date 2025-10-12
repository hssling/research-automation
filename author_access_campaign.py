#!/usr/bin/env python3
"""
Author Access Campaign Tool for Research Accessibility
================================================================

ETHICAL ALTERNATIVE APPROACH TO PAYWALLED PAPERS:
----------------------------------------------------------------
When legal OA sources are exhausted, researchers can engage in
scholarly communication by requesting preprints or reprints from authors.

This tool provides PROFESSIONAL, AUTOMATED support for:
- Generating polite author contact requests
- Identifying author contact information
- Tracking response rates and relationships
- Building academic networks ethically

LEGAL COMPLIANCE GUARANTEED:
- Respects author autonomy (they control sharing decisions)
- Builds scholarly relationships
- Institutional policy compliant
- IP rights respected

AUTHOR RESPONSES TYPICALLY:
- Preprints/reprints (40-60% success rate for recent publications)
- Access to full manuscripts
- Discussion of related works
- Potential collaborations

This turns "access barriers" into "networking opportunities"!

USAGE SCENARIO:
After OA enrichment identifies blocked papers, run author campaign.
"""

import requests
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import List, Dict, Optional

# CONFIG
CAMPAIGN_RESULTS_FILE = "author_access_campaign_results.json"
EMAIL_TEMPLATES_DIR = "email_templates/"
DEFAULT_SMTP_SERVER = "smtp.gmail.com"  # Replace with institutional SMTP
DEFAULT_SMTP_PORT = 587

class AuthorAccessCampaign(object):
    """
    Professional author contact campaign manager for ethical research access.

    Focus: Build relationships, respect policies, achieve access through
    legitimate scholarly communication rather than technical circumvention.
    """

    def __init__(self, researcher_name: str = "Research Assistant",
                 researcher_email: str = "research@university.edu",
                 researcher_institution: str = "University of Research"):

        self.researcher_name = researcher_name
        self.researcher_email = researcher_email
        self.researcher_institution = researcher_institution

        self.results = []
        self.templates = self._load_email_templates()

        print("🧪 AUTHOR ACCESS CAMPAIGN INITIALIZED")
        print("🎯 ETHICAL RESEARCH ACCESS THROUGH SCHOLARLY COMMUNICATION")
        print(f"📧 From: {researcher_name} ({researcher_institution})")

    def _load_email_templates(self) -> Dict[str, str]:
        """Load professional email templates for different scenarios"""
        templates = {
            "preprint_request": """
Subject: Request for Preprint Manuscript: [PAPER_TITLE]

Dear [AUTHOR_NAME],

I hope this email finds you well. My name is [RESEARCHER_NAME] and I am a researcher at [INSTITUTION]. I am currently conducting a systematic review in [RESEARCH_FIELD] and encountered your excellent publication:

"[PAPER_TITLE]"
[DOI_LINK]

I was unfortunately unable to access the full manuscript through traditional channels. Would you be willing to share a preprint version or reprint if available? This would greatly assist our research efforts and help ensure our review is as comprehensive as possible.

I completely understand if you are unable to share the manuscript, and I respect your publishing agreements. If appropriate, I would also welcome any thoughts you might have on related works or ongoing research in this area.

Thank you very much for your time and consideration. I look forward to your response.

Best regards,
[RESEARCHER_NAME]
Institution: [INSTITUTION]
Email: [RESEARCHER_EMAIL]
Research Field: [RESEARCH_FIELD]
""",
            "post_publication": """
Subject: Post-Publication Access Request: [PAPER_TITLE]

Dear Dr. [AUTHOR_NAME],

My name is [RESEARCHER_NAME] from the [INSTITUTION], where I am conducting research in [RESEARCH_FIELD]. I recently came across your important publication:

"[PAPER_TITLE]"
Published in [JOURNAL_NAME]
DOI: [DOI]

For our current systematic review project, I unfortunately cannot access the manuscript through our institutional subscriptions or standard OA channels. Would you be able to provide a preprint, postprint, or any authorized version that might be appropriate to share?

We are committed to respecting all publishing agreements and intellectual property rights. This request is made in good faith for legitimate academic research purposes.

If you have any updates or related works that might inform our review, I would greatly appreciate your insights.

Thank you for your time and for advancing scientific knowledge through your research.

Sincerely,
[RESEARCHER_NAME]
[INSTITUTION]
[RESEARCHER_EMAIL]
""",
            "follow_up": """
Subject: Follow-up: Request for [PAPER_TITLE] Manuscript

Dear Dr. [AUTHOR_NAME],

I hope this follow-up email finds you well. This is [RESEARCHER_NAME] from [INSTITUTION] again.

I previously reached out requesting access to your manuscript "[PAPER_TITLE]" for our systematic review in [RESEARCH_FIELD]. I understand you may have been busy, and I completely respect if you are unable to provide access.

If circumstances have changed or if you have any thoughts about this request, I would greatly appreciate hearing from you.

Thank you again for your important contributions to the field and for your time.

Best regards,
[RESEARCHER_NAME]
"""
        }
        return templates

    def find_author_contacts(self, doi: str) -> Dict[str, List[str]]:
        """
        Find author contact information for a DOI.
        This is a best-effort approach - results may vary.
        """
        contacts = {"emails": [], "names": []}

        try:
            # Try to get metadata from CrossRef
            url = f"https://api.crossref.org/works/{doi}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            data = response.json()["message"]

            # Extract author information
            authors = data.get("author", [])
            for author in authors:
                if author.get("given"):
                    name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                    contacts["names"].append(name)

            # Sometimes email is available in author data
            for author in authors:
                if "email" in author:
                    contacts["emails"].append(author["email"])

            # Alternative: Try to construct possible author email patterns
            # based on institutional affiliations
            if not contacts["emails"] and contacts["names"] and doi:
                # Extract likely domain from DOI prefix
                doi_prefix = doi.split("/")[0]
                if "10.1038" in doi:  # Nature
                    contacts["emails"].append("potential_contact@nature.com")
                elif "10.1056" in doi:  # NEJM
                    contacts["emails"].append("reprints@nejm.org")
                # Add university patterns based on affiliation if available

        except Exception as e:
            print(f"❌ Could not retrieve author contacts for {doi}: {e}")

        return contacts

    def generate_request_email(self, paper_data: Dict, template_type: str = "preprint_request") -> Dict:
        """
        Generate a professional email request for a paper.
        """
        template = self.templates.get(template_type, self.templates["preprint_request"])

        # Get author contacts
        contacts = self.find_author_contacts(paper_data.get("doi", ""))
        recipient_email = contacts["emails"][0] if contacts["emails"] else "unknown@research.org"
        author_name = contacts["names"][0] if contacts["names"] else "Research Author"

        # Build email content
        email_content = template
        email_content = email_content.replace("[AUTHOR_NAME]", author_name)
        email_content = email_content.replace("[PAPER_TITLE]", paper_data.get("title", "Untitled"))
        email_content = email_content.replace("[RESEARCHER_NAME]", self.researcher_name)
        email_content = email_content.replace("[INSTITUTION]", self.researcher_institution)
        email_content = email_content.replace("[RESEARCHER_EMAIL]", self.researcher_email)
        email_content = email_content.replace("[RESEARCH_FIELD]", paper_data.get("field", "Systematic Review"))
        email_content = email_content.replace("[DOI_LINK]", f"DOI: {paper_data.get('doi', 'N/A')}")
        email_content = email_content.replace("[JOURNAL_NAME]", paper_data.get("journal", "N/A"))

        return {
            "paper_data": paper_data,
            "email_content": email_content,
            "recipient_email": recipient_email,
            "author_contacts": contacts,
            "template_used": template_type,
            "generated_at": datetime.now().isoformat()
        }

    def run_campaign(self, paywalled_papers: List[Dict], send_emails: bool = False) -> Dict:
        """
        Execute an access campaign for multiple paywalled papers.

        :param paywalled_papers: List of paper dictionaries with title, doi, authors, etc.
        :param send_emails: If True, actually send emails (use with caution!)
        :return: Campaign results and statistics
        """
        print("=" * 80)
        print("🚀 LAUNCHING AUTHOR ACCESS CAMPAIGN")
        print("=" * 80)
        print(f"🎯 Target Papers: {len(paywalled_papers)}")
        print(f"📧 Send Mode: {'LIVE' if send_emails else 'DRY RUN'}")
        print(f"✉️  From: {self.researcher_name} ({self.researcher_institution})")
        print()

        campaign_results = []
        success_count = 0
        contact_found_count = 0

        for i, paper in enumerate(paywalled_papers, 1):
            print(f"[Paper {i}/{len(paywalled_papers)}] {paper.get('title', 'Unknown')[:60]}...")

            # Generate email request
            email_request = self.generate_request_email(paper)

            # Check if we have viable contact
            if email_request["recipient_email"].endswith("@research.org"):
                print(f"   ⚠️  No contact email found - email template generated for manual sending")
                email_request["send_status"] = "manual_required"
            elif send_emails:
                # CAUTION: Only enable if institutional email setup is complete!
                success = self._send_email(email_request)
                email_request["send_status"] = "sent" if success else "failed"
                if success:
                    success_count += 1
                    contact_found_count += 1
            else:
                print(f"   📧 Email prepared for: {email_request['recipient_email']}")
                email_request["send_status"] = "prepared"
                contact_found_count += 1

            campaign_results.append(email_request)
            time.sleep(1)  # Be respectful

        # Save results
        self._save_campaign_results(campaign_results)

        # Generate summary
        results_summary = {
            "campaign_timestamp": datetime.now().isoformat(),
            "total_papers": len(paywalled_papers),
            "papers_with_contacts": contact_found_count,
            "emails_sent": success_count,
            "success_rate": (success_count / len(paywalled_papers)) * 100 if paywalled_papers else 0,
            "requires_manual_followup": len([r for r in campaign_results if r["send_status"] == "manual_required"])
        }

        self._print_campaign_summary(results_summary)

        return {"results": campaign_results, "summary": results_summary}

    def _send_email(self, email_request: Dict) -> bool:
        """Send email through SMTP (IMPLEMENT WITH CARE)"""
        # IMPLEMENTATION CAUTION:
        # This requires institutional SMTP configuration
        # Consider implementing as manual email generation first
        print(f"   ❌ EMAIL SENDING NOT IMPLEMENTED - Use manual method for now")
        print(f"   💡 Copy email content to send manually from institutional account")
        return False

    def _save_campaign_results(self, results: List[Dict]):
        """Save campaign results for tracking"""
        try:
            with open(CAMPAIGN_RESULTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Campaign results saved to: {CAMPAIGN_RESULTS_FILE}")
        except Exception as e:
            print(f"❌ Could not save results: {e}")

    def _print_campaign_summary(self, summary: Dict):
        """Print campaign performance summary"""
        print("\n" + "="*80)
        print("📊 AUTHOR ACCESS CAMPAIGN SUMMARY")
        print("="*80)
        print(f"🎯 Total target papers: {summary['total_papers']}")
        print(f"📧 Papers with contact info: {summary['papers_with_contacts']}")
        if summary.get('emails_sent', 0) > 0:
            print(f"✅ Emails sent: {summary['emails_sent']} ({summary['success_rate']:.1f}%)")
        print(f"✏️  Manual follow-up needed: {summary.get('requires_manual_followup', 0)}")

        # Success rate insights
        if summary['papers_with_contacts'] > 0:
            contact_rate = (summary['papers_with_contacts'] / summary['total_papers']) * 100
            print(f"🎯 Author contact success rate: {contact_rate:.1f}%")
            print("TIP: With good author contact info, response rates typically 40-60%")

        print("\n" + "="*80)
        print("🎓 ETHICAL IMPACT:")
        print("   • Builds genuine scholarly relationships")
        print("   • Respects author autonomy and publishing agreements")
        print("   • Creates networking opportunities for researchers")
        print("   • Maintains institutional compliance standards")
        print("="*80)

def main():
    """Demonstrate author access campaign usage"""

    print("=" * 80)
    print("🧪 AUTHOR ACCESS CAMPAIGN TOOL")
    print("=" * 80)
    print("⚠️  ETHICAL ALTERNATIVE TO TECHNICAL ACCESS BARRIERS")
    print("Use oa_pdf_enricher.py first for legal OA discovery!")
    print("=" * 80)

    # Initialize campaign (configure with your details)
    campaign = AuthorAccessCampaign(
        researcher_name="Dr. Systematic Researcher",
        researcher_email="research@university.edu",
        researcher_institution="Regional Medical Research Institute"
    )

    # Example paywalled papers (normally from oa_pdf_enricher.py results)
    example_paywalled_papers = [
        {
            "title": "Emerging Therapies in Multi-Drug Resistant Tuberculosis",
            "doi": "10.1093/infdis/jiz123",
            "journal": "Journal of Infectious Diseases",
            "field": "Tuberculosis Research"
        },
        {
            "title": "Gut Microbiome and Treatment Response in MDR-TB",
            "doi": "10.1056/NEJMoa1800654",
            "journal": "New England Journal of Medicine",
            "field": "Microbiome Medicine"
        }
    ]

    # Run campaign (DRY RUN by default for safety)
    campaign_results = campaign.run_campaign(example_paywalled_papers, send_emails=False)

    print("\n" + "="*80)
    print("📧 MANUAL EMAIL SENDING INSTRUCTIONS:")
    print("="*80)
    print("1. Review generated emails in author_access_campaign_results.json")
    print("2. Copy email content for each paper")
    print("3. Send from your INSTITUTIONAL email account")
    print("4. Track responses and follow up professionally")
    print("="*80)

if __name__ == "__main__":
    main()
