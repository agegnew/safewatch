from urllib import request
import os
import flask
from flask import request, redirect, url_for, render_template
#import test3
from werkzeug.utils import secure_filename


app = flask.Flask(__name__)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv'}

def check_video_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def get_home_page():
    return flask.render_template("index.html")


@app.route("/stored-videos", methods=['GET', 'POST'])
def get_stored_videos():
    if request.method == 'POST':
        if 'video' not in request.files:
            return 'No file part'
        file = request.files['video']

        if file.filename == '':
            return 'No selected file'

        # Если файл корректен, сохраняем его
        if file and check_video_format(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('get_stored_videos'))

    # Отображаем страницу с видео
    return render_template("stored_videos.html")

# @app.route("/stored-videos")
# def get_stored_video(video_id):
#     test3.play_video_with_detection()

@app.route("/live-feed")
def get_live_feed():
    return flask.render_template("live-feed.html")

@app.route("/emergency-counts")
def get_emergency_counts():
    return flask.render_template("emergency-counts.html")



app.run(host="0.0.0.0", port=5000)