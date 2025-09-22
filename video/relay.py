from flask import Blueprint, Response, stream_with_context
import requests

video_bp = Blueprint("video", __name__)

VIDEO_STREAM_URL = "http://10.53.237.174:8080/video"  # Update with correct phone IP

@video_bp.route("/video_feed")
def video_feed():
    def generate():
        with requests.get(VIDEO_STREAM_URL, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
    return Response(stream_with_context(generate()), mimetype='multipart/x-mixed-replace; boundary=frame')
