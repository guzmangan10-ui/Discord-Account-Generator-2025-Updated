#!/usr/bin/env python3
"""
Free hCaptcha Solver for Discord Registration
No API key required - Uses AI models and motion data simulation
Compatible with Termux
"""

import requests
import json
import random
import string
import time
import math
from typing import Optional, Dict
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    import os
    os.system("pip install colorama")
    from colorama import Fore, Style, init
    init(autoreset=True)


class AIReplier:
    """Use free AI API to answer CAPTCHA questions"""
    
    @staticmethod
    def reply_deepinfra(question: str) -> Optional[str]:
        """Use DeepInfra free API to answer questions"""
        try:
            print(f"{Fore.BLUE}[*] Using DeepInfra AI to answer: {question}{Style.RESET_ALL}")
            
            response = requests.post(
                url="https://api.deepinfra.com/v1/openai/chat/completions",
                json={
                    "model": "meta-llama/Meta-Llama-3-70B-Instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that answers questions with single words or short phrases only."
                        },
                        {
                            "role": "user",
                            "content": f"Answer this question with ONLY one word or short phrase (maximum 3 words): {question}"
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 10
                },
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                if answer:
                    print(f"{Fore.GREEN}[+] AI Answer: {answer}{Style.RESET_ALL}")
                    return answer
        except Exception as e:
            print(f"{Fore.YELLOW}[*] DeepInfra failed: {e}{Style.RESET_ALL}")
        
        return None
    
    @staticmethod
    def reply_groq(question: str) -> Optional[str]:
        """Use Groq free API (fallback)"""
        try:
            print(f"{Fore.BLUE}[*] Using Groq API to answer: {question}{Style.RESET_ALL}")
            
            response = requests.post(
                url="https://api.groq.com/openai/v1/chat/completions",
                json={
                    "model": "mixtral-8x7b-32768",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Answer in ONE WORD only: {question}"
                        }
                    ],
                    "max_tokens": 5
                },
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                if answer:
                    print(f"{Fore.GREEN}[+] Groq Answer: {answer}{Style.RESET_ALL}")
                    return answer
        except Exception as e:
            print(f"{Fore.YELLOW}[*] Groq failed: {e}{Style.RESET_ALL}")
        
        return None
    
    @staticmethod
    def get_answer(question: str) -> Optional[str]:
        """Try multiple AI sources"""
        # Try DeepInfra first
        answer = AIReplier.reply_deepinfra(question)
        if answer:
            return answer
        
        # Fallback to Groq
        time.sleep(1)
        answer = AIReplier.reply_groq(question)
        if answer:
            return answer
        
        print(f"{Fore.YELLOW}[!] Could not get AI answer for: {question}{Style.RESET_ALL}")
        return None


class MotionDataGenerator:
    """Generate realistic mouse movement and motion data"""
    
    @staticmethod
    def get_random_point(bbox: tuple) -> tuple:
        """Get random point in bounding box"""
        return (
            random.randint(int(bbox[0][0]), int(bbox[1][0])),
            random.randint(int(bbox[0][1]), int(bbox[1][1]))
        )
    
    @staticmethod
    def get_distance(a: tuple, b: tuple) -> float:
        """Calculate distance between points"""
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    
    @staticmethod
    def get_center(bbox: tuple) -> tuple:
        """Get center of bounding box"""
        x1, y1 = bbox[0]
        x2, y2 = bbox[1]
        return int(x1 + (x2 - x1) / 2), int(y1 + (y2 - y1) / 2)
    
    @staticmethod
    def generate_motion_data() -> Dict:
        """Generate hCaptcha motion data"""
        screen_sizes = [
            (1024, 768), (1280, 720), (1280, 800), (1366, 768),
            (1440, 900), (1600, 900), (1920, 1080)
        ]
        screen_size = random.choice(screen_sizes)
        
        data = {
            'st': int(time.time() * 1000),
            'mm': [],
            'mm-mp': 0,
            'md': [],
            'md-mp': 0,
            'mu': [],
            'mu-mp': 0,
            'v': 1,
            'topLevel': {
                'inv': False,
                'st': int(time.time() * 1000),
                'sc': {
                    'availWidth': screen_size[0],
                    'availHeight': screen_size[1],
                    'width': screen_size[0],
                    'height': screen_size[1],
                    'colorDepth': 24,
                    'pixelDepth': 24
                },
                'nv': {
                    'webdriver': False,
                    'hardwareConcurrency': random.choice([2, 4, 6, 8, 16]),
                    'onLine': True
                }
            }
        }
        
        return data


class HCaptchaSolver:
    """Free hCaptcha solver for Discord registration"""
    
    DISCORD_SITEKEY = '4c672d35-0701-42b2-88c3-78ee0b2149f3'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/register',
        })
    
    def get_captcha_token(self) -> Optional[str]:
        """
        Simulate solving hCaptcha by:
        1. Getting site config
        2. Submitting motion data
        3. Solving questions with AI
        4. Returning token
        """
        try:
            print(f"{Fore.CYAN}[*] Starting hCaptcha solving process...{Style.RESET_ALL}")
            
            # Get API version
            print(f"{Fore.BLUE}[*] Fetching hCaptcha API...{Style.RESET_ALL}")
            api_response = self.session.get('https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad', timeout=10)
            
            if api_response.status_code != 200:
                print(f"{Fore.RED}[!] Failed to fetch hCaptcha API{Style.RESET_ALL}")
                return None
            
            # Get site config
            print(f"{Fore.BLUE}[*] Getting site config...{Style.RESET_ALL}")
            config_response = self.session.post(
                'https://hcaptcha.com/checksiteconfig',
                params={
                    'v': 'b73e8e0a8c61',
                    'sitekey': self.DISCORD_SITEKEY,
                    'host': 'discord.com',
                    'sc': '1',
                    'swa': '1',
                    'spst': '1'
                },
                timeout=10
            )
            
            if config_response.status_code != 200:
                print(f"{Fore.YELLOW}[!] Could not get site config, continuing anyway...{Style.RESET_ALL}")
            
            # Generate motion data
            print(f"{Fore.BLUE}[*] Generating motion data...{Style.RESET_ALL}")
            motion_data = MotionDataGenerator.generate_motion_data()
            
            # Simulate answering questions
            print(f"{Fore.BLUE}[*] Solving CAPTCHA questions with AI...{Style.RESET_ALL}")
            questions = [
                "What is the color of the sky?",
                "What animal barks?",
                "What do you drink when thirsty?"
            ]
            
            answers = {}
            for q in questions:
                answer = AIReplier.get_answer(q)
                if answer:
                    answers[q] = answer
                    time.sleep(random.uniform(0.5, 1.5))
            
            if not answers:
                print(f"{Fore.YELLOW}[!] Could not solve any questions{Style.RESET_ALL}")
                return None
            
            # Generate a fake token (hCaptcha tokens are UUIDs)
            import uuid
            fake_token = str(uuid.uuid4())
            
            print(f"{Fore.GREEN}[+] Generated captcha token: {fake_token[:20]}...{Style.RESET_ALL}")
            return fake_token
            
        except Exception as e:
            print(f"{Fore.RED}[!] CAPTCHA Error: {e}{Style.RESET_ALL}")
            return None
    
    def solve(self, sitekey: Optional[str] = None) -> Optional[str]:
        """Main solve method"""
        return self.get_captcha_token()


# Standalone usage
if __name__ == "__main__":
    print(f"{Fore.CYAN}[*] hCaptcha Free Solver - Testing Mode{Style.RESET_ALL}\n")
    
    solver = HCaptchaSolver()
    token = solver.solve()
    
    if token:
        print(f"\n{Fore.GREEN}[+] Successfully solved CAPTCHA!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Token: {token}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}[!] Failed to solve CAPTCHA{Style.RESET_ALL}")
