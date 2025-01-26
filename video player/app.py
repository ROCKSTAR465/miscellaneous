from flask import Flask, request, jsonify
import whisper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to generate subtitles
def generate_subtitles(video_path, output_path="subtitles.vtt", model_type="base"):
    try:
        model = whisper.load_model(model_type)
        result = model.transcribe(video_path, task="translate")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")  # WebVTT header
            for segment in result["segments"]:
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"]
                f.write(f"{start_time} --> {end_time}\n{text}\n\n")

        return True
    except Exception as e:
        print(f"Error generating subtitles: {e}")
        return False

# Function to format timestamps
def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Route to handle video upload and subtitle generation
@app.route('/generate-subtitles', methods=['POST'])
def handle_subtitle_generation():
    if 'video' not in request.files:
        return jsonify({"error": "No video file uploaded."}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    # Save the uploaded video file
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video_file.filename))
    video_file.save(video_path)

    # Generate subtitles
    subtitle_file = os.path.join(app.config['UPLOAD_FOLDER'], "subtitles.vtt")
    if generate_subtitles(video_path, subtitle_file):
        return jsonify({"subtitleUrl": f"/{subtitle_file}"}), 200
    else:
        return jsonify({"error": "Failed to generate subtitles."}), 500

# Serve static files (subtitles)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return app.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)