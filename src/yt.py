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
    except Exception as e:
        return None

@app.route('/api/ytmp4', methods=['GET'])
def youtube_video_url():
    youtube_link = request.args.get('link')
    
    if not youtube_link:
        return jsonify({
            "error": "Please provide a YouTube link using the \"link\" parameter",
            "usage": "http://localhost:3000/api/ytmp4?link=<youtube_url>"
        }), 400
    
    download_url = get_download_url(youtube_link, audio_only=False)
    
    if download_url:
        return jsonify({
            "success": True,
            "download_url": download_url,
            "original_url": youtube_link,
            "type": "video"
        }), 200
    
    return jsonify({
        "success": False,
        "error": "Failed to get download URL. The video might be private or the URL might be invalid."
    }), 400

@app.route('/api/ytmp3', methods=['GET'])
def youtube_audio_url():
    youtube_link = request.args.get('link')
    
    if not youtube_link:
        return jsonify({
            "error": "Please provide a YouTube link using the \"link\" parameter",
            "usage": "http://localhost:3000/api/ytmp3?link=<youtube_url>"
        }), 400
    
    download_url = get_download_url(youtube_link, audio_only=True)
    
    if download_url:
        return jsonify({
            "success": True,
            "download_url": download_url,
            "original_url": youtube_link,
            "type": "audio"
        }), 200
    
    return jsonify({
        "success": False,
        "error": "Failed to get download URL. The video might be private or the URL might be invalid."
    }), 400

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
