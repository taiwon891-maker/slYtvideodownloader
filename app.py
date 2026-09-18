import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
YOUTUBE_API_KEY = "AIzaSyAj_ZB8TOSQViO5MYQAfYEnf-T9LlcuFks"

@app.route('/')
def index():
    return render_template('index.html')

# ভিডিও সার্চ
@app.route('/search')
def search():
    query = request.args.get('q', 'Bangla hit songs')
    page_token = request.args.get('pageToken', '')
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=12&q={query}&type=video&pageToken={page_token}&key={YOUTUBE_API_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        videos = []
        for item in data.get('items', []):
            if 'snippet' in item and 'videoId' in item.get('id', {}):
                videos.append({
                    "title": item['snippet']['title'],
                    "thumbnail": item['snippet']['thumbnails']['high']['url'],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "videoId": item['id']['videoId'],
                    "channel": item['snippet']['channelTitle']
                })
        return jsonify({"videos": videos, "nextPageToken": data.get('nextPageToken', '')})
    except Exception as e:
        return jsonify({"videos": [], "nextPageToken": "", "error": str(e)})

# সরাসরি ডাউনলোডের জন্য API
@app.route('/get_download_stream')
def get_download_stream():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '720')
    
    if not video_url:
        return jsonify({"error": "Video URL missing"}), 400

    q_format = "720" if quality == "720p" else ("1080" if quality == "1080p" else "mp3")

    # API Request to generate server stream
    try:
        cobalt_api = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": video_url,
            "vQuality": q_format,
            "isAudioOnly": True if quality == 'mp3' else False
        }
        res = requests.post(cobalt_api, json=payload, headers=headers, timeout=10)
        data = res.json()
        
        if "url" in data:
            return jsonify({"status": "success", "download_url": data["url"]})
        else:
            return jsonify({"status": "error", "message": "Download limit reached or link invalid."}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
