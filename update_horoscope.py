#!/usr/bin/env python3
"""
Scrapes daily horoscopes for all zodiac signs and saves to horoscope.json
"""

import json
import os
from horoscope import HoroscopeScraper


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Saved {path}")


def main():
    print("=" * 60)
    print("Scraping Daily Horoscopes")
    print("=" * 60)

    scraper = HoroscopeScraper(delay=1.0)
    signs = list(scraper.DAILY_URLS.keys())
    combined = {}

    for sign in signs:
        print(f"\nScraping {sign.upper()}...")
        daily = scraper.scrape_sign(sign)
        if daily:
            combined[sign] = {
                'date': daily.get('date', ''),
                'summary': daily.get('summary', ''),
                'ratings': daily.get('ratings', {}),
                'scraped_at': daily.get('scraped_at', '')
            }

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'horoscope.json')
    save_json(output_path, combined)
    print(f"\nDone! Scraped {len(combined)} signs.")


if __name__ == "__main__":
    main()
