import os
import json
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_admin_key_123'  # সেশন সিকিউরিটির জন্য

YOUTUBE_API_KEY = "AIzaSyAj_ZB8TOSQViO5MYQAfYEnf-T9LlcuFks"
SETTINGS_FILE = "settings.json"

# অ্যাডমিন লগইন তথ্য
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "adsterra_head_script": "<!-- Adsterra Head Script -->",
            "adsterra_banner_script": "<!-- Adsterra Banner Script -->",
            "custom_header_title": "YouTube Player & Downloader"
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=4)
        return default_settings
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return jsonঅ্যাডমিন প্যানেল, ডায়নামিক অ্যাডস সেটিংস ও ইউটিউব সার্চ ফিচারসহ সম্পূর্ণ `app.py` ফাইলের কোড নিচে দেওয়া হলো:

```python
import os
import json
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
# সেশনের জন্য সিক্রেট কি
app.secret_key = 'super_secret_admin_key_123'

# ইউটিউব এপিআই কি
YOUTUBE_API_KEY = "AIzaSyAj_ZB8TOSQViO5MYQAfYEnf-T9LlcuFks"
SETTINGS_FILE = "settings.json"

# অ্যাডমিন লগইন তথ্য
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def load_settings():
    """সেটিংস ফাইল লোড করা"""
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "adsterra_head_script": "<!-- Adsterra Head Script -->",
            "adsterra_banner_script": "<!-- Adsterra Banner Script -->",
            "custom_header_title": "YouTube Player & Downloader"
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=4)
        return default_settings
    
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "adsterra_head_script": "",
            "adsterra_banner_script": "",
            "custom_header_title": "YouTube Player & Downloader"
        }

def save_settings(data):
    """সেটিংস ফাইলে ডাটা সেভ করা"""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    """মূল হোম পেজ"""
    settings = load_settings()
    return render_template('index.html', settings=settings)

@app.route('/search')
def search():
    """ইউটিউব সার্চ এপিআই রুট"""
    query = request.args.get('q', 'Bangla hit songs')
    page_token = request.args.get('pageToken', '')
    url = f"[https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=12&q=](https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=12&q=){query}&type=video&pageToken={page_token}&key={YOUTUBE_API_KEY}"
    

    
