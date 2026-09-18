import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
YOUTUBE_API_KEY = "AIzaSyAj_ZB8TOSQViO5MYQAfYEnf-T9LlcuFks"

@app.route('/')
def index():
    return render_template('index.html')

# ভিডিও সার্চ API
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

# ওয়ার্কিং ডাইরেক্ট ডাউনলোডার
@app.route('/get_download_stream')
def get_download_stream():
    video_id = request.args.get('id')
    quality = request.args.get('quality', '720p')
    
    if not video_id:
        return jsonify({"status": "error", "message": "Video ID missing"}), 400

    try:
        # YouTube direct stream extractor API
        api_url = f"https://yt-download-api.vercel.app/api/download?id={video_id}"
        response = requests.get(api_url, timeout=12)
        res_data = response.json()

        if res_data.get("status") == "success" or "formats" in res_data:
            formats = res_data.get("formats", [])
            download_url = None

            if quality == 'mp3':
                for fmt in formats:
                    if fmt.get('isAudioOnly') or 'audio' in fmt.get('mimeType', ''):
                        download_url = fmt.get('url')
                        break
            else:
                target_height = 1080 if quality == '1080p' else 720
                for fmt in formats:
                    if fmt.get('height') == target_height and fmt.get('hasAudio', True):
                        download_url = fmt.get('url')
                        break
            
            if not download_url and len(formats) > 0:
                download_url = formats[0].get('url')

            if download_url:
                return jsonify({"status": "success", "download_url": download_url})

        return jsonify({"status": "error", "message": "Download link failed"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
