#!/usr/bin/env python3
"""
Discord Account Generator 2025 - Updated for Latest Discord API
Compatible with Termux, Python 3.8+
Features: Latest Discord API v10, Batch generation, hCaptcha solver
"""

import requests
import json
import os
import sys
import time
import random
import string
from datetime import datetime
from typing import Dict, Optional

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    from colorama import Fore, Style, init
    init(autoreset=True)

try:
    from fake_useragent import UserAgent
except ImportError:
    os.system("pip install fake-useragent")
    from fake_useragent import UserAgent

# Import hCaptcha solver
try:
    from hcaptcha_solver import hCaptchaSolver
    SOLVER_AVAILABLE = True
except ImportError:
    print(f"{Fore.YELLOW}[!] hcaptcha_solver.py not found{Style.RESET_ALL}")
    SOLVER_AVAILABLE = False


class DiscordAPIv10:
    """Discord API v10 handler with hCaptcha support"""
    
    BASE_URL = "https://discord.com/api/v10"
    
    def __init__(self, proxy: Optional[str] = None):
        self.session = requests.Session()
        self.fingerprint = None
        self.captcha_solver = hCaptchaSolver() if SOLVER_AVAILABLE else None
        
        try:
            self.user_agent = UserAgent().random
        except Exception:
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        if proxy:
            proxy_url = f'http://{proxy}' if '://' not in proxy else proxy
            self.session.proxies.update({
                'http': proxy_url,
                'https': proxy_url
            })
        
        self._setup_headers()
    
    def _setup_headers(self) -> None:
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/register',
            'Content-Type': 'application/json',
        })
    
    def get_fingerprint(self) -> Optional[str]:
        """Get Discord fingerprint"""
        try:
            print(f"{Fore.BLUE}[*] Getting fingerprint...{Style.RESET_ALL}")
            response = self.session.get(
                f"{self.BASE_URL}/experiments",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self.fingerprint = data.get('fingerprint')
                if self.fingerprint:
                    print(f"{Fore.GREEN}[+] Fingerprint: {self.fingerprint[:20]}...{Style.RESET_ALL}")
                    return self.fingerprint
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Fingerprint Error: {e}{Style.RESET_ALL}")
        
        # Fallback fingerprint
        self.fingerprint = "fallback_fp_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
        print(f"{Fore.YELLOW}[!] Using fallback fingerprint{Style.RESET_ALL}")
        return self.fingerprint
    
    def register(self, email: str, username: str, password: str) -> Optional[Dict]:
        """Register account with hCaptcha handling"""
        try:
            print(f"{Fore.BLUE}[*] Registering: {username}...{Style.RESET_ALL}")
            
            if not self.fingerprint:
                self.get_fingerprint()
            
            payload = {
                "fingerprint": self.fingerprint,
                "email": email,
                "username": username,
                "password": password,
                "date_of_birth": "1990-01-15",
                "consent": True,
                "promotional_email_opt_in": False,
            }
            
            # Initial registration attempt
            response = self.session.post(
                f"{self.BASE_URL}/auth/register",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 201:
                result = response.json()
                token = result.get('token')
                if token:
                    print(f"{Fore.GREEN}[+] SUCCESS! Token: {token[:40]}...{Style.RESET_ALL}")
                    return result
            
            elif response.status_code == 400:
                error_data = response.json()
                
                # Check for hCaptcha requirement
                if 'captcha_key' in error_data or 'captcha_sitekey' in error_data:
                    print(f"{Fore.YELLOW}[!] hCaptcha required!{Style.RESET_ALL}")
                    
                    if not self.captcha_solver:
                        print(f"{Fore.RED}[!] CAPTCHA solver not available{Style.RESET_ALL}")
                        return None
                    
                    # Solve hCaptcha
                    print(f"{Fore.CYAN}[*] Solving hCaptcha...{Style.RESET_ALL}")
                    captcha_token = self.captcha_solver.solve(error_data)
                    
                    if captcha_token:
                        print(f"{Fore.CYAN}[*] Retrying with CAPTCHA token...{Style.RESET_ALL}")
                        payload['captcha_key'] = captcha_token
                        
                        retry_response = self.session.post(
                            f"{self.BASE_URL}/auth/register",
                            json=payload,
                            timeout=15
                        )
                        
                        if retry_response.status_code == 201:
                            result = retry_response.json()
                            token = result.get('token')
                            if token:
                                print(f"{Fore.GREEN}[+] SUCCESS with CAPTCHA! Token: {token[:40]}...{Style.RESET_ALL}")
                                return result
                        else:
                            print(f"{Fore.RED}[!] Registration failed: {retry_response.status_code}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[!] Failed to solve CAPTCHA{Style.RESET_ALL}")
                    
                    return None
                else:
                    msg = error_data.get('message', str(error_data)[:100])
                    print(f"{Fore.RED}[!] Error: {msg}{Style.RESET_ALL}")
                    return None
            
            else:
                print(f"{Fore.RED}[!] Failed: {response.status_code}{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[!] Registration Error: {e}{Style.RESET_ALL}")
            return None


class EmailGenerator:
    DOMAINS = ['tempmail.com', '10minutemail.com', 'throwaway.email', 'yopmail.com', 'mailinator.com']
    
    @staticmethod
    def generate() -> str:
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        return f"{username}@{random.choice(EmailGenerator.DOMAINS)}"


class UsernameGenerator:
    ADJECTIVES = ['happy', 'cool', 'dark', 'swift', 'smart', 'brave', 'wild', 'free']
    NOUNS = ['dragon', 'phoenix', 'tiger', 'wolf', 'eagle', 'panda', 'fox', 'raven']
    
    @staticmethod
    def generate() -> str:
        return f"{random.choice(UsernameGenerator.ADJECTIVES)}_{random.choice(UsernameGenerator.NOUNS)}_{random.randint(100, 9999)}"


class AccountGenerator:
    def __init__(self, proxy: Optional[str] = None):
        self.accounts = []
        self.api = DiscordAPIv10(proxy=proxy)
    
    def generate_account(self) -> Optional[Dict]:
        email = EmailGenerator.generate()
        username = UsernameGenerator.generate()
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()", k=16))
        
        print(f"\n{Fore.CYAN}[=] Email: {email}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[=] Username: {username}{Style.RESET_ALL}")
        
        result = self.api.register(email, username, password)
        
        if result:
            account = {
                'email': email,
                'username': username,
                'password': password,
                'token': result.get('token'),
                'id': result.get('id'),
                'timestamp': datetime.now().isoformat()
            }
            self.accounts.append(account)
            return account
        return None
    
    def generate_batch(self, count: int = 5, delay: float = 2.0):
        print(f"\n{Fore.CYAN}[*] Generating {count} accounts (delay: {delay}s)...{Style.RESET_ALL}\n")
        for i in range(count):
            print(f"{Fore.YELLOW}[{i+1}/{count}]{Style.RESET_ALL}")
            self.generate_account()
            if i < count - 1:
                time.sleep(delay)
    
    def save(self, filename: str = "accounts.json"):
        with open(filename, 'w') as f:
            json.dump(self.accounts, f, indent=2)
        print(f"\n{Fore.GREEN}[+] Saved {len(self.accounts)} accounts to {filename}{Style.RESET_ALL}")
    
    def display(self):
        if not self.accounts:
            print(f"{Fore.YELLOW}[*] No accounts generated{Style.RESET_ALL}")
            return
        print(f"\n{Fore.CYAN}[=] Generated {len(self.accounts)} Accounts{Style.RESET_ALL}")
        for i, acc in enumerate(self.accounts, 1):
            token = acc.get('token', 'N/A')
            token_display = f"{token[:40]}..." if token and len(str(token)) > 40 else token
            print(f"\n{Fore.YELLOW}[{i}]{Style.RESET_ALL}")
            print(f"  Email: {acc['email']}")
            print(f"  Username: {acc['username']}")
            print(f"  Token: {token_display}")


def main():
    print(f"""
{Fore.CYAN}
╔════════════════════════════════════════════════════════════╗
║  Discord Account Generator 2025 - Updated                  ║
║  API v10 • Termux Ready • hCaptcha Solver                  ║
╚════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    if SOLVER_AVAILABLE:
        print(f"{Fore.GREEN}[+] hCaptcha solver ready{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}[!] hCaptcha solver not available{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}[?] Menu:{Style.RESET_ALL}")
    print("1. Generate 1 account")
    print("2. Generate batch accounts")
    print("3. Exit")
    
    choice = input(f"\n{Fore.CYAN}[>] Choice: {Style.RESET_ALL}").strip()
    
    generator = AccountGenerator()
    
    if choice == '1':
        generator.generate_account()
        generator.display()
        generator.save()
    
    elif choice == '2':
        count = int(input(f"{Fore.CYAN}[>] How many? (default 5): {Style.RESET_ALL}") or "5")
        delay = float(input(f"{Fore.CYAN}[>] Delay seconds (default 2): {Style.RESET_ALL}") or "2")
        generator.generate_batch(count, delay)
        generator.display()
        generator.save()
    
    elif choice == '3':
        print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
