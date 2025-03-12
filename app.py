from flask import Flask, request, send_file, render_template
import yt_dlp
import os

# Create a downloads folder if it doesn't exist
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template("index.html")

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

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


