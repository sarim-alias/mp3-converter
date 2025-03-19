from flask import Flask, request, send_file, render_template, after_this_request
import yt_dlp
import os
import threading
import time

# Create a downloads folder if it doesn't exist
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/id')
def index_id():
    return render_template("index.html", lang="id")  # Indonesian version

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get("url")
    if not video_url:
        return "Error: No URL provided"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            filename = os.path.splitext(filename)[0] + ".mp3"  # Ensure file has .mp3 extension
    except Exception as e:
        return f"Error downloading audio: {str(e)}"

    # Delete file after sending response
    @after_this_request
    def remove_file(response):
        threading.Thread(target=delete_file_after_delay, args=(filename, 60)).start()
        return response

    return send_file(filename, as_attachment=True)

def delete_file_after_delay(filename, delay=60):
    """Delete the file after a delay (default: 60 seconds)"""
    time.sleep(delay)
    try:
        os.remove(filename)
        print(f"Deleted: {filename}")
    except Exception as e:
        print(f"Error deleting file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)