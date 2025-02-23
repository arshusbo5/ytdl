import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_download_url(url, audio_only=False):
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'best',
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']
    except Exception:
        return None

@app.route('/api/ytmp4', methods=['GET'])
def youtube_video_url():
    youtube_link = request.args.get('link')
    
    if not youtube_link:
        return jsonify({"error": "Missing 'link' parameter"}), 400
    
    download_url = get_download_url(youtube_link, audio_only=False)
    
    if download_url:
        return jsonify({
            "success": True,
            "download_url": download_url,
            "original_url": youtube_link,
            "type": "video"
        }), 200
    
    return jsonify({"success": False, "error": "Failed to get download URL"}), 400

@app.route('/api/ytmp3', methods=['GET'])
def youtube_audio_url():
    youtube_link = request.args.get('link')
    
    if not youtube_link:
        return jsonify({"error": "Missing 'link' parameter"}), 400
    
    download_url = get_download_url(youtube_link, audio_only=True)
    
    if download_url:
        return jsonify({
            "success": True,
            "download_url": download_url,
            "original_url": youtube_link,
            "type": "audio"
        }), 200
    
    return jsonify({"success": False, "error": "Failed to get download URL"}), 400

if __name__ == '__main__':
   port = int(os.environ.get("PORT", 8080))  # Use Railway's assigned port or default to 3000
    app.run(host='0.0.0.0', port=port)
