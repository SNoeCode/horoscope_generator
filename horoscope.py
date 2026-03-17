"""
HuggingFace Daily Horoscope Generator
Generates daily horoscopes for all zodiac signs using the HuggingFace Inference API
"""

import requests
import os
from datetime import datetime
from typing import Dict, Optional
import time


class HoroscopeGenerator:

    MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

    SIGNS = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
        'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
    ]

    SIGN_TRAITS = {
        'aries': 'bold, energetic, and pioneering',
        'taurus': 'grounded, patient, and determined',
        'gemini': 'curious, adaptable, and communicative',
        'cancer': 'intuitive, nurturing, and emotional',
        'leo': 'confident, creative, and generous',
        'virgo': 'analytical, practical, and detail-oriented',
        'libra': 'balanced, diplomatic, and charming',
        'scorpio': 'intense, passionate, and transformative',
        'sagittarius': 'adventurous, optimistic, and philosophical',
        'capricorn': 'ambitious, disciplined, and persistent',
        'aquarius': 'innovative, independent, and humanitarian',
        'pisces': 'dreamy, empathetic, and artistic'
    }

    def __init__(self):
        self.token = os.environ.get('HF_TOKEN', '')
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

    def build_prompt(self, sign):
        today = datetime.now().strftime('%B %d, %Y')
        traits = self.SIGN_TRAITS.get(sign, '')
        prompt = (
            "[INST] Write a daily horoscope for " + sign.capitalize() + " for " + today + ". "
            + sign.capitalize() + " is " + traits + ". "
            "Write 3-4 sentences, mystical and encouraging tone, "
            "covering love, career, and personal growth. "
            "Return only the horoscope paragraph, no headings or labels. [/INST]"
        )
        return prompt

    def generate_horoscope(self, sign):
        if sign not in self.SIGNS:
            print("Invalid sign: " + sign)
            return None

        prompt = self.build_prompt(sign)
        payload = {
            'inputs': prompt,
            'parameters': {
                'max_new_tokens': 200,
                'temperature': 0.85,
                'do_sample': True,
                'return_full_text': False
            }
        }

        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '').strip()
            else:
                text = str(result).strip()

            # wait 2 seconds between calls so we dont hit rate limits
            time.sleep(2)

            return {
                'date': datetime.now().strftime('%B %d, %Y'),
                'summary': text,
                'ratings': {},
                'scraped_at': datetime.now().isoformat()
            }

        except requests.RequestException as e:
            print("Error generating horoscope for " + sign + ": " + str(e))
            return None
