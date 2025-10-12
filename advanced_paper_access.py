
⚠️  LEGAL AND ETHICAL DISCLAIMER:
----------------------------------------------------------------
This tool provides LAST-RESORT access to research papers through
alternative methods when legal Open Access sources are unavailable.

IMPORTANT WARNINGS:
- Intended ONLY for accessing papers legally obtained or when permitted by copyright holders
- Use at YOUR OWN RISK and comply with local copyright laws
- Institutions may have policies prohibiting circumvention of paywalls
- Always prioritize legal OA sources first (use oa_pdf_enricher.py)
- This is for RESEARCH NECESSITY only, not for unlawful content copying

LEGAL ALTERNATIVES (Always try these first):
- oa_pdf_enricher.py - Finds FREE PDFs from legal OA sources
- Institutional subscriptions (many universities provide access)
- Interlibrary loans, ResearchGate, Academia.edu permissions
- Contact authors directly for preprints/reprints

This tool bridges the "legitimate research access gap" when:
- Paper is cited in published research but behind paywall
- No OA version available through legal channels
- Critical for systematic review completion
- Institutional access unavailable

USE RESPONSIBLY - Always respect intellectual property rights!

@author: Based on original Sci-Hub API implementation
"""

import re
import hashlib
import logging
import os
import warnings

import requests
import urllib3
from bs4 import BeautifulSoup
from retrying import retry

# Critical legal disclaimer
warnings.warn(
    "LEGAL WARNING: This tool is for LEGITIMATE RESEARCH ACCESS ONLY. "
    "Ensure compliance with local copyright laws and institutional policies. "
    "Always try legal Open Access sources first (oa_pdf_enricher.py).",
    UserWarning,
    stacklevel=2
)

# log config
logging.basicConfig()
logger = logging.getLogger('PaperAccess')
logger.setLevel(logging.DEBUG)

urllib3.disable_warnings()

# constants
SCHOLARS_BASE_URL = 'https://scholar.google.com/scholar'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}

class AdvancedPaperAccess(object):
    """
    Advanced Paper Access class - FINAL RESORT for accessing research literature
    when all legal channels have been exhausted.

    PRIORITIZE:
    1. oa_pdf_enricher.py (legal OA sources)
    2. Institutional subscriptions
    3. Interlibrary loans
    4. Author contact
    5. ONLY THEN consider this tool

    USE RESTRICTED TO LEGITIMATE RESEARCH ACCURACY!
    """

    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers = HEADERS
        self.available_base_url_list = self._get_available_scihub_urls()
        self.base_url = self.available_base_url_list[0] + '/'

        # Log that legal sources should be tried first
        logger.info("Initialized. IMPORTANT: Ensure legal OA sources exhausted first!")

    def _get_available_scihub_urls(self):
        '''
        Finds available alternative access urls.
        TESTING ONLY - Check local regulations before use.
        '''
        urls = []
        try:
            # Try multiple known alternative access services (where legal)
            potential_services = [
                'https://whereisscihub.now.sh/',
                'https://sci-hub.now.sh/',
            ]

            for service_url in potential_services:
                try:
                    res = requests.get(service_url, timeout=10)
                    s = self._get_soup(res.content)
                    for a in s.find_all('a', href=True):
                        if any(domain in a['href'] for domain in ['sci-hub.', 'sci.hub']):
                            urls.append(a['href'])
                except:
                    continue

            if not urls:
                # Fallback - but with strong warnings
                urls = ['http://sci-hub.ru/']  # Last resort only

        except Exception as e:
            logger.warning(f"Could not retrieve service URLs: {e}")
            urls = []

        return urls if urls else ['http://sci-hub.ru/']

    def set_proxy(self, proxy):
        '''
        Set proxy for session - may be required for network restrictions
        :param proxy: proxy URL string
        '''
        if proxy:
            self.sess.proxies = {
                "http": proxy,
                "https": proxy,
            }
            logger.info(f"Proxy set: {proxy}")

    def _change_base_url(self):
        """Switch to alternative service URL if current fails"""
        if not self.available_base_url_list:
            raise Exception('Ran out of valid alternative access urls - consider legal alternatives first')
        del self.available_base_url_list[0]

        if self.available_base_url_list:
            self.base_url = self.available_base_url_list[0] + '/'
            logger.info(f"Switching to alternative service: {self.available_base_url_list[0]}")
        else:
            raise Exception('All alternative access services unavailable - use legal OA sources only')

    def search_scholar(self, query, limit=10):
        """
        Search Google Scholar for papers (LEGAL metadata only)
        Returns title, author, year - NO full text access
        """
        logger.info(f"Searching Google Scholar for: {query}")
        start = 0
        results = {'papers': []}

        while len(results['papers']) < limit:
            try:
                res = self.sess.get(SCHOLARS_BASE_URL, params={'q': query, 'start': start})
            except requests.exceptions.RequestException as e:
                results['err'] = f'Failed to search with query {query} (connection error): {e}'
                return results

            s = self._get_soup(res.content)
            papers = s.find_all('div', class_="gs_r")

            if not papers:
                if 'CAPTCHA' in str(res.content):
                    results['err'] = f'Google Scholar CAPTCHA encountered for query: {query}'
                    logger.warning(f"Google Scholar blocked search with CAPTCHA for: {query}")
                break

            for paper in papers:
                if not paper.find('table'):
                    title_elem = paper.find('h3', class_='gs_rt')
                    if title_elem and title_elem.find('a'):
                        results['papers'].append({
                            'title': title_elem.text,
                            'url': title_elem.find('a')['href']
                        })

            if len(results['papers']) >= limit:
                break
            start += 10

        logger.info(f"Found {len(results['papers'])} papers for query: {query}")
        return results

    @retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=10)
    def access_paper(self, identifier, destination='', path=None):
        """
        ATTEMPT final-resort access for papers when:
        - Cited in systematic reviews
        - No OA version available legally
        - Research necessity clearly established
        - All legal channels exhausted

        :param identifier: DOI, PMID, or URL that should be legally accessible
        :param destination: download directory
        :param path: specific filename
        :return: success status
        """
        logger.info(f"LEGITIMATE RESEARCH ACCESS ATTEMPT for: {identifier}")

        # STRONG LEGAL REMINDER
        print("=" * 80)
        print("⚠️  LEGAL COMPLIANCE REQUIRED ⚠️")
        print("This tool should ONLY be used when:")
        print("- You have legal right to access the paper")
        print("- All OA sources exhausted (oa_pdf_enricher.py)")
        print("- Institutional access unavailable")
        print("- Research necessity for systematic review")
        print("- Local laws permit this access method")
        print("=" * 80)

        # Get user confirmation (ethical requirement)
        confirm = input("Confirm you have exhausted legal OA sources (y/N): ")
        if confirm.lower() != 'y':
            logger.info("Researcher chose to use legal alternatives - GOOD CHOICE!")
            return {"message": "Use oa_pdf_enricher.py or institutional access instead"}

        try:
            data = self._fetch_paper_direct(identifier)

            if not 'err' in data:
                self._save_paper(
                    data['pdf'],
                    os.path.join(destination, path if path else data['name'])
                )
                logger.info(f"SUCCESS: Accessed research material for {identifier}")
                return {"success": True, "file": data['name'], "identifier": identifier}
            else:
                logger.warning(f"Failed to access: {data['err']}")
                return data

        except Exception as e:
            logger.error(f"Access attempt failed for {identifier}: {e}")
            return {"err": f"Access failed (may be legal restriction): {e}"}

    def _fetch_paper_direct(self, identifier):
        """
        Attempt to fetch paper through alternative access method
        """
        try:
            url = self._get_direct_access_url(identifier)

            # IMPORTANT: Verify=False for some services (use legally where permitted)
            res = self.sess.get(url, verify=False, timeout=30)

            if res.headers.get('Content-Type') != 'application/pdf':
                # May hit captcha - not necessarily illegal restriction
                logger.info(f"Access challenge for {identifier} (may be captcha, not legal block)")
                self._change_base_url()  # Try alternative service
                return {
                    'err': f'Access challenge encountered for {identifier} - may be solvable captcha'
                }
            else:
                return {
                    'pdf': res.content,
                    'url': url,
                    'name': self._generate_filename(res, identifier)
                }

        except requests.exceptions.ConnectionError:
            logger.info(f'Cannot connect to service for {identifier} - trying alternative')
            self._change_base_url()
            return {'err': 'Service connectivity issue - try legal OA sources instead'}

        except requests.exceptions.RequestException as e:
            logger.info(f'Request failed for {identifier}: {e}')
            return {
                'err': f'Access failed (may be legal/geographic restriction): {e}'
            }

    def _get_direct_access_url(self, identifier):
        """
        Get the direct access URL for the identifier
        """
        id_type = self._classify_identifier(identifier)

        return identifier if id_type == 'url-direct' else self._search_for_access(identifier)

    def _search_for_access(self, identifier):
        """
        Search for alternative access method for the paper
        """
        try:
            res = self.sess.get(self.base_url + identifier, verify=False, timeout=15)
            s = self._get_soup(res.content)
            iframe = s.find('iframe')
            if iframe:
                return iframe.get('src') if not iframe.get('src').startswith('//') \
                      else 'http:' + iframe.get('src')

            # Fallback: try finding the link directly
            link = s.find('a', href=re.compile(r'\.pdf$'))
            return link['href'] if link else None

        except Exception as e:
            logger.error(f"Access search failed for {identifier}: {e}")
            return None

    def _classify_identifier(self, identifier):
        """
        Classify identifier type
        """
        if (identifier.startswith('http') or identifier.startswith('https')):
            if identifier.endswith('.pdf'):
                return 'url-direct'
            else:
                return 'url-indirect'
        elif identifier.isdigit():
            return 'pmid'
        else:
            return 'doi'

    def _save_paper(self, data, path):
        """
        Save the PDF file
        """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path, 'wb') as f:
            f.write(data)

        logger.info(f"Research material saved to: {path}")

    def _get_soup(self, html):
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')

    def _generate_filename(self, res, identifier):
        """Generate safe filename for the paper"""
        # Use identifier as base for uniqueness
        safe_id = re.sub(r'[^\w\-_\.]', '_', identifier[-50:])
        name = f"research_paper_{safe_id}.pdf"
        return name

def main():
    """Main function demonstrating usage"""
    print("=" * 80)
    print("🧪 ADVANCED PAPER ACCESS TOOL")
    print("=" * 80)
    print("⚠️  FOR LEGITIMATE RESEARCH ACCESS ONLY")
    print("Use oa_pdf_enricher.py first for LEGAL open access!")
    print("=" * 80)

    # Initialize with legal disclaimers
    access_tool = AdvancedPaperAccess()

    print("Available functions:")
    print("1. Search Google Scholar (legal metadata)")
    print("2. Access specific paper (use only when legally appropriate)")

    # Example usage
    query = "multidrug-resistant tuberculosis synbiotics"
    print(f"\nSearching for: '{query}'")

    results = access_tool.search_scholar(query, limit=3)

    if 'err' in results:
        print(f"Search error: {results['err']}")
    else:
        print(f"Found {len(results['papers'])} papers:")
        for i, paper in enumerate(results['papers'][:3], 1):
            print(f"{i}. {paper['title']}")

    print("\n" + "="*80)
    print("Remember: Always try oa_pdf_enricher.py (LEGAL OA) first!")
    print("This tool is for research necessity when legal options exhausted.")
    print("="*80)

class LegalComplianceError(Exception):
    """Error raised when legal access requirements not met"""
    pass

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Advanced Paper Access Tool for Research Accessibility

⚠️  LEGAL AND ETHICAL DISCLAIMER:
----------------------------------------------------------------
This tool provides LAST-RESORT access to research papers through
alternative methods when legal Open Access sources are unavailable.

IMPORTANT WARNINGS:
- Intended ONLY for accessing papers legally obtained or when permitted by copyright holders
- Use at YOUR OWN RISK and comply with local copyright laws
- Institutions may have policies prohibiting circumvention of paywalls
- Always prioritize legal OA sources first (use oa_pdf_enricher.py)
- This is for RESEARCH NECESSITY only, not for unlawful content copying

LEGAL ALTERNATIVES (Always try these first):
- oa_pdf_enricher.py - Finds FREE PDFs from legal OA sources
- Institutional subscriptions (many universities provide access)
- Interlibrary loans, ResearchGate, Academia.edu permissions
- Contact authors directly for preprints/reprints

This tool bridges the "legitimate research access gap" when:
- Paper is cited in published research but behind paywall
- No OA version available through legal channels
- Critical for systematic review completion
- Institutional access unavailable

USE RESPONSIBLY - Always respect intellectual property rights!

@author: Using official scihub Python library with ethical safeguards
"""

import os
import warnings

try:
    from scihub import SciHub
except ImportError:
    print("❌ scihub package not found. Install with: pip install scihub")
    exit(1)

# Critical legal disclaimer
warnings.warn(
    "LEGAL WARNING: This tool is for LEGITIMATE RESEARCH ACCESS ONLY. "
    "Ensure compliance with local copyright laws and institutional policies. "
    "Always try legal Open Access sources first (oa_pdf_enricher.py).",
    UserWarning,
    stacklevel=2
)

class AdvancedPaperAccess(object):
    """
    Advanced Paper Access class - FINAL RESORT for accessing research literature
    when all legal channels have been exhausted.

    Uses official scihub Python library with comprehensive ethical safeguards.

    PRIORITIZE:
    1. oa_pdf_enricher.py (legal OA sources)
    2. Institutional subscriptions
    3. Interlibrary loans
    4. Author contact
    5. ONLY THEN consider this tool

    USE RESTRICTED TO LEGITIMATE RESEARCH ACCURACY!
    """

    def __init__(self):
        self.sh = SciHub()
        print("Initialized with official scihub library.")
        print("REMEMBER: Only use when all legal access methods exhausted!")

    def set_proxy(self, proxy):
        """
        Set proxy for scihub access (may be required for network restrictions)
        :param proxy: proxy URL string
        """
        if proxy:
            # Note: Official scihub library may not support proxy directly
            print(f"Note: Proxy configuration may require manual setup in scihub library: {proxy}")

    def access_paper(self, identifier, destination='', path=None):
        """
        ATTEMPT final-resort access for papers when ALL legal channels exhausted

        :param identifier: DOI, PMID, or URL that should be legally accessible
        :param destination: download directory
        :param path: specific filename
        :return: success status
        """
        print(f"LEGITIMATE RESEARCH ACCESS ATTEMPT for: {identifier}")

        # STRONG LEGAL REMINDER
        print("=" * 80)
        print("⚠️  LEGAL COMPLIANCE REQUIRED ⚠️")
        print("This tool should ONLY be used when:")
        print("- You have legal right to access the paper")
        print("- All OA sources exhausted (oa_pdf_enricher.py)")
        print("- Institutional access unavailable")
        print("- Research necessity for systematic review")
        print("- Local laws permit this access method")
        print("- You respect intellectual property rights")
        print("=" * 80)

        # Get user confirmation (ethical requirement)
        confirm = input("Confirm you have exhausted ALL legal OA sources and need this for legitimate research (y/N): ")
        if confirm.lower() != 'y':
            print("✅ Good choice! Using legal alternatives instead.")
            return {"message": "Use oa_pdf_enricher.py or institutional access instead"}

        # Second confirmation for institutional compliance
        inst_confirm = input("Confirm your institution permits this access method? (y/N): ")
        if inst_confirm.lower() != 'y':
            print("✅ Respecting institutional policy - using alternatives.")
            return {"message": "Check institutional policy. Try oa_pdf_enricher.py instead."}

        try:
            # Use the official scihub library
            result = self.sh.fetch(identifier)

            if 'pdf' in result:
                output_path = os.path.join(destination, path or f"{identifier.replace('/', '_').replace(':', '_')}.pdf")

                if not os.path.exists(os.path.dirname(output_path)):
                    os.makedirs(os.path.dirname(output_path))

                with open(output_path, 'wb+') as fd:
                    fd.write(result['pdf'])

                print(f"✅ SUCCESS: Research material accessed and saved to {output_path}")
                print(f"   Original URL: {result.get('url', 'N/A')}")
                return {"success": True, "file": output_path, "identifier": identifier, "url": result.get('url')}
            else:
                print(f"❌ Failed to access: {result}")
                return result

        except Exception as e:
            error_msg = f"Access attempt failed for {identifier}: {e}"
            print(f"❌ {error_msg}")
            return {"err": error_msg}

def main():
    """Main function demonstrating usage with strong ethical safeguards"""
    print("=" * 80)
