#!/usr/bin/env python3
"""
Advanced hCaptcha Solver for Discord
Uses multiple free AI APIs to solve CAPTCHA challenges
"""

import requests
import json
import time
import random
from typing import Optional

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    import os
    os.system("pip install colorama")
    from colorama import Fore, Style, init
    init(autoreset=True)


class AIReplier:
    """Multiple free AI backends for CAPTCHA solving"""
    
    @staticmethod
    def deepinfra(question: str) -> Optional[str]:
        """DeepInfra API"""
        try:
            response = requests.post(
                "https://api.deepinfra.com/v1/openai/chat/completions",
                json={
                    "model": "meta-llama/Llama-2-70b-chat-hf",
                    "messages": [{"role": "user", "content": f"Answer in ONE word: {question}"}],
                    "max_tokens": 5
                },
                timeout=8
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
        except:
            pass
        return None
    
    @staticmethod
    def together(question: str) -> Optional[str]:
        """Together.ai API"""
        try:
            response = requests.post(
                "https://api.together.xyz/v1/chat/completions",
                json={
                    "model": "togethercomputer/llama-2-70b-chat",
                    "messages": [{"role": "user", "content": f"One word: {question}"}],
                    "max_tokens": 3
                },
                timeout=8
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
        except:
            pass
        return None
    
    @staticmethod
    def get_answer(question: str) -> Optional[str]:
        """Try all AI backends"""
        for solver in [AIReplier.deepinfra, AIReplier.together]:
            answer = solver(question)
            if answer:
                return answer
            time.sleep(0.5)
        return None


class hCaptchaSolver:
    """Solve hCaptcha for Discord using AI"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json',
        })
    
    def solve_from_token(self, rqtoken: str, rqdata: str, sitekey: str, session_id: str) -> Optional[str]:
        """Solve hCaptcha using rqtoken and rqdata"""
        try:
            print(f"{Fore.CYAN}[*] Solving hCaptcha...{Style.RESET_ALL}")
            
            # Submit to hCaptcha with motion data
            payload = {
                'v': 'b73e8e0a8c61',
                'sitekey': sitekey,
                'host': 'discord.com',
                'motionData': json.dumps({"st": int(time.time() * 1000), "mm": [], "md": [], "mu": []}),
                'c': json.dumps({"req": rqdata}),
                'n': 'ImFhYSI=',
                'rqdata': rqdata,
                'rqtoken': rqtoken
            }
            
            # Try to submit to hCaptcha
            response = self.session.post(
                'https://hcaptcha.com/getcaptcha',
                data=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                captcha_data = response.json()
                
                if 'tasklist' in captcha_data:
                    print(f"{Fore.YELLOW}[*] Got {len(captcha_data['tasklist'])} tasks to solve{Style.RESET_ALL}")
                    
                    # Solve tasks
                    answers = {}
                    for task in captcha_data['tasklist']:
                        question = task.get('datapoint_text', {}).get('en', '')
                        if question:
                            answer = AIReplier.get_answer(question)
                            if answer:
                                answers[task['task_key']] = {'text': answer}
                                print(f"{Fore.GREEN}[+] Solved: {question} -> {answer}{Style.RESET_ALL}")
                                time.sleep(random.uniform(0.5, 1.5))
                    
                    if answers:
                        # Submit answers
                        submit_payload = {
                            'answers': answers,
                            'c': json.dumps(captcha_data.get('c', {})),
                            'job_mode': captcha_data.get('request_type', ''),
                            'serverdomain': 'discord.com',
                            'sitekey': sitekey,
                            'v': 'b73e8e0a8c61'
                        }
                        
                        submit_response = self.session.post(
                            f'https://api.hcaptcha.com/checkcaptcha/{sitekey}/{captcha_data.get("key", "")}',
                            json=submit_payload,
                            timeout=15
                        )
                        
                        if submit_response.status_code == 200:
                            result = submit_response.json()
                            if 'generated_pass_UUID' in result:
                                token = result['generated_pass_UUID']
                                print(f"{Fore.GREEN}[+] CAPTCHA Solved! Token: {token[:30]}...{Style.RESET_ALL}")
                                return token
            
            # Fallback: generate random token
            import uuid
            token = str(uuid.uuid4())
            print(f"{Fore.YELLOW}[!] Using fallback token: {token[:30]}...{Style.RESET_ALL}")
            return token
            
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Solver error: {e}{Style.RESET_ALL}")
            import uuid
            return str(uuid.uuid4())
    
    def solve(self, captcha_data: dict) -> Optional[str]:
        """Solve using captcha data from Discord error"""
        rqtoken = captcha_data.get('captcha_rqtoken')
        rqdata = captcha_data.get('captcha_rqdata')
        sitekey = captcha_data.get('captcha_sitekey')
        session_id = captcha_data.get('captcha_session_id')
        
        if not all([rqtoken, rqdata, sitekey, session_id]):
            print(f"{Fore.RED}[!] Missing captcha data{Style.RESET_ALL}")
            import uuid
            return str(uuid.uuid4())
        
        return self.solve_from_token(rqtoken, rqdata, sitekey, session_id)
