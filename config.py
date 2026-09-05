# Configuration file

# API Settings
API_VERSION = "v10"
BASE_URL = "https://discord.com/api"

# Generation Settings
DEFAULT_BATCH_SIZE = 5
DEFAULT_DELAY = 2.0

# Email Domains
EMAIL_DOMAINS = [
    'tempmail.com',
    '10minutemail.com',
    'throwaway.email',
    'yopmail.com',
    'mailinator.com',
]

# Output
OUTPUT_FILE = 'accounts.json'

# Proxy (optional)
USE_PROXY = False
PROXY = None  # "ip:port"

# Captcha Settings
CAPTCHA_ENABLED = True

# Cloudflare Turnstile Settings (Discord's current captcha)
CLOUDFLARE_TURNSTILE_SITE_KEY = "a9b5fb07-92ff-493f-86fe-352a2803b3df"
CLOUDFLARE_TURNSTILE_SECRET_KEY = "0x4AARyUeBIcQWLv3G2Smart59Oy56w1irD4xJ86MD92"

# 2Captcha API Settings (for solving Turnstile captchas)
TWO_CAPTCHA_API_KEY = "YOUR_2CAPTCHA_API_KEY"
TWO_CAPTCHA_API_URL = "http://2captcha.com/api/upload"
TWO_CAPTCHA_SOLVE_URL = "http://2captcha.com/api/res.php"

# CapSolver API Settings (for solving Turnstile)
CAPSOLVER_API_KEY = "YOUR_CAPSOLVER_API_KEY"

# Anti-Captcha Settings
ANTI_CAPTCHA_API_KEY = "YOUR_ANTICAPTCHA_API_KEY"

# Captcha Timeout (seconds)
CAPTCHA_TIMEOUT = 60

# Captcha Retry Attempts
CAPTCHA_RETRY_ATTEMPTS = 3
