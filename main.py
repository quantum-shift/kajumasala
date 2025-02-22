from flask import Flask, request, jsonify
import logging
from generateDemoSteps import create_steps_prompt
from audio import gen_audio, gen_transcript, crawl
from generateDemoVideo import generateDemoVideo as gen_video
from audio.process_logs import process_logs
from overlay.merge_av import merge_video_audio
import uuid
import traceback
import asyncio

# setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# def gen_video(context):
#     logging.info("Generating video")
#     pass

@app.route('/generate', methods=['POST'])
def run():
    try:
        user_query = request.json.get('user_query')
        if not user_query:
            return jsonify({'status': 'error', 'message': 'Missing user_query'}), 400
        
        request_id = uuid.uuid4()

        context = {'user_query': user_query, 'request_id': request_id}
        logging.info(f"Received user query: {user_query}")
        crawl(context)
        create_steps_prompt(context)
        context['start_url'] = 'https://elevenlabs.io/app'
        asyncio.run(gen_video(context))
        process_logs(context)
        gen_transcript(context)
        gen_audio(context)
        merge_video_audio(context)

        if not context.get('final_video_path'):
            return jsonify({'status': 'error', 'message': 'Missing final_video_path in context'}), 500

        final_video_path = context.get('final_video_path')
        return jsonify({'status': 'success', 'request_id': request_id, 'final_video_path': final_video_path}), 200
    except Exception as e:
        logging.error(f"Error processing request: {str(e), traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)