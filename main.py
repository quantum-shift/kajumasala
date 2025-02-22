from flask import Flask, request, jsonify
import logging
from generateDemoSteps import create_steps_prompt
import uuid

# setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def gen_video(context):
    logging.info("Generating video")
    pass

def gen_transcript(context):
    logging.info("Generating transcript")
    pass

def gen_audio(context):
    logging.info("Generating audio")
    pass

def overlay_audio_to_video(context):
    logging.info("Overlaying audio to video")
    pass

@app.route('/generate', methods=['POST'])
def run():
    try:
        user_query = request.json.get('user_query')
        if not user_query:
            return jsonify({'status': 'error', 'message': 'Missing user_query'}), 400
        
        request_id = uuid.uuid4()

        context = {'user_query': user_query, 'request_id': request_id}
        logging.info(f"Received user query: {user_query}")

        create_steps_prompt(context)
        gen_video(context)
        gen_transcript(context)
        gen_audio(context)
        overlay_audio_to_video(context)

        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)