from flask import Flask

app = Flask(__name__)

# Step function placeholders
def create_steps_prompt():
    pass

def gen_video():
    pass

def gen_transcript():
    pass

def gen_audio():
    pass

def overlay_audio_to_video():
    pass

@app.route('/run', methods=['GET'])
def run():
    # Sequentially call all functions, piping outputs
    create_steps_prompt_data = create_steps_prompt()
    er_gen_video_data = gen_video()
    gen_transcript_data = gen_transcript()
    gen_audio_data = gen_audio()
    overlay_audio_to_video_data = overlay_audio_to_video()
    returns