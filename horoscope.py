"""
Cafe Astrology Daily Horoscope Scraper
Scrapes daily horoscopes for all zodiac signs from cafeastrology.com
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, Optional
import time
import re


class HoroscopeScraper:
    """Scraper for Cafe Astrology daily horoscopes"""

    BASE_URL = "https://cafeastrology.com"

    DAILY_URLS = {
        'aries': '/ariesdailyhoroscope.html',
        'taurus': '/taurusdailyhoroscope.html',
        'gemini': '/geminidailyhoroscope.html',
        'cancer': '/cancerdailyhoroscope.html',
        'leo': '/leodailyhoroscope.html',
        'virgo': '/virgodailyhoroscope.html',
        'libra': '/libradailyhoroscope.html',
        'scorpio': '/scorpiodailyhoroscope.html',
        'sagittarius': '/sagittariusdailyhoroscope.html',
        'capricorn': '/capricorndailyhoroscope.html',
        'aquarius': '/aquariusdailyhoroscope.html',
        'pisces': '/piscesdailyhoroscope.html'
    }

    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_daily_horoscope(self, soup: BeautifulSoup, sign: str) -> Optional[Dict]:
        try:
            date_text = None
            for elem in soup.find_all(['h4', 'h3', 'p']):
                text = elem.get_text(strip=True)
                if re.search(r'[A-Z][a-z]+ \d{1,2}, \d{4}', text):
                    date_text = text
                    break

            horoscope_text = None
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 100 and ('dear' in text.lower() or 'moon' in text.lower()):
                    horoscope_text = text
                    break

            if not horoscope_text:
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 200:
                        horoscope_text = text
                        break

            ratings = {}
            ratings_text = soup.find(string=re.compile(r'Creativity:.*Love:.*Business:'))
            if ratings_text:
                for label in ['creativity', 'love', 'business']:
                    match = re.search(rf'{label.capitalize()}:\s*(\w+)', ratings_text, re.I)
                    if match:
                        ratings[label] = match.group(1)

            return {
                'date': date_text or datetime.now().strftime('%B %d, %Y'),
                'summary': horoscope_text or "Horoscope text not found",
                'ratings': ratings,
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error extracting horoscope for {sign}: {e}")
            return None

    def scrape_sign(self, sign: str) -> Optional[Dict]:
        if sign not in self.DAILY_URLS:
            print(f"Invalid sign: {sign}")
            return None

        url = self.BASE_URL + self.DAILY_URLS[sign]
        print(f"  Scraping {sign.capitalize()}...")

        soup = self.fetch_page(url)
        if not soup:
            return None

        horoscope = self.extract_daily_horoscope(soup, sign)
        time.sleep(self.delay)
        return horoscope
