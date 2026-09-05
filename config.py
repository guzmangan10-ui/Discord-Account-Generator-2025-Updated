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

# reCAPTCHA v2 Settings
RECAPTCHA_V2_SITE_KEY = "6Le-wvkSAAAAAPBMRTvw0Q75SrRu0d4Hc5qdC2kJ"
RECAPTCHA_V2_SECRET_KEY = "6Le-wvkSAAAAAPBMRTvw0Q75SrRu0d4Hc5qdC2kJ"

# reCAPTCHA v3 Settings
RECAPTCHA_V3_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_V3_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

# hCaptcha Settings
HCAPTCHA_SITE_KEY = "10000000-ffff-ffff-ffff-000000000001"
HCAPTCHA_SECRET_KEY = "0x4AARyUeBIcQWLv3G2Smart59Oy56w1irD4xJ86MD92"

# Cloudflare Turnstile Settings
CLOUDFLARE_TURNSTILE_SITE_KEY = "1x00000000000000000000AA"
CLOUDFLARE_TURNSTILE_SECRET_KEY = "1x0000000000000000000000000000000AA"

# 2Captcha API Settings (for solving captchas)
TWO_CAPTCHA_API_KEY = "YOUR_2CAPTCHA_API_KEY"
TWO_CAPTCHA_API_URL = "http://2captcha.com/api/upload"

# Anti-Captcha Settings
ANTI_CAPTCHA_API_KEY = "YOUR_ANTICAPTCHA_API_KEY"

# Captcha Timeout (seconds)
CAPTCHA_TIMEOUT = 30

# Captcha Retry Attempts
CAPTCHA_RETRY_ATTEMPTS = 3
