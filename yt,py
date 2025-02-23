from flask import Flask, request, jsonify
import yt_dlp

app = Flask(_name_)

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

# MP4 Video Endpoint
@app.route('/api/ytmp4', methods=['GET'])
def youtube_video_url():
    youtube_link = request.args.get('link')
    
    if not youtube_link:
        response = {
            "error": "Please provide a YouTube link using the \"link\" parameter",
            "usage": "http://localhost:3000/api/ytmp4?link=<youtube_url>"
        }
        return jsonify(response), 400
    
    download_url = get_download_url(youtube_link, audio_only=False)
    
    if download_url:
        response = {
            "success": True,
            "download_url": download_url,
            "original_url": youtube_link,
            "type": "video"
        }
        return jsonify(response), 200
    
    response = {
        "success": False,
        "error": "Failed to get download URL. The video might be private or the URL might be invalid."
    }
    return jsonify(response), 400

# MP3 Audio Endpoint
@app.route('/api/ytmp3', methods=['GET'])
def youtube_audio_url():
    youtube_link = request.args.get('link')
    
    if not youtube_link:
        response = {
            "error": "Please provide a YouTube link using the \"link\" parameter",
            "usage": "http://localhost:3000/api/ytmp3?link=<youtube_url>"
        }
        return jsonify(response), 400
    
    download_url = get_download_url(youtube_link, audio_only=True)
    
    if download_url:
        response = {
            "success": True,
            "download_url": download_url,
            "original_url": youtube_link,
            "type": "audio"
        }
        return jsonify(response), 200
    
    response = {
        "success": False,
        "error": "Failed to get download URL. The video might be private or the URL might be invalid."
    }
    return jsonify(response), 400

if _name_ == '_main_':
    app.run(host='localhost', port=3000, debug=True)
