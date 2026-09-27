import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
YOUTUBE_API_KEY = "AIzaSyAj_ZB8TOSQViO5MYQAfYEnf-T9LlcuFks"

@app.route('/')
def index():
    return render_template('index.html')

# ইউটিউব সার্চ এপিআই
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

# সরাসরি স্ট্রিম ইউআরএল বের করার এপিআই (ইমবেড ব্লক বাইপাস)
@app.route('/get_stream')
def get_stream():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"status": "error", "message": "Video ID missing"}), 400

    try:
        # Piped API থেকে ভিডিও স্ট্রিম রিট্রাইভ
        piped_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
        r = requests.get(piped_url, timeout=10)
        data = r.json()

        stream_url = None
        # ভিডিও স্ট্রিম খোঁজা
        for stream in data.get('videoStreams', []):
            if stream.get('videoOnly') == False and stream.get('url'):
                stream_url = stream.get('url')
                break

        if stream_url:
            return jsonify({"status": "success", "stream_url": stream_url})
        else:
            return jsonify({"status": "error", "message": "Stream not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
