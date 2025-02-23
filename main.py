from flask import Flask, request, jsonify, Response, stream_with_context
import logging
from generateDemoSteps import create_steps_prompt
from audio import gen_audio, gen_transcript, crawl
from generateDemoVideo import generateDemoVideo as gen_video
from audio.process_logs import process_logs
from overlay.merge_av import merge_video_audio
import uuid
import traceback
import asyncio
from flask_cors import CORS
import json

# setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# def gen_video(context):
#     logging.info("Generating video")
#     pass

def handle_generate():
    try:
        user_query = request.args.get('user_query')  # Use args, not json
        language = request.args.get('language')  # Use args, not json

        if not user_query or not language:
            yield f"data: {json.dumps({'status': 'error', 'message': 'Missing required data'})}\n\n"
            return

        request_id = str(uuid.uuid4())
        context = {'user_query': user_query, 'request_id': request_id, 'language': language}
        logging.info(f"Received user query: {user_query}")

        yield f"data: {json.dumps({'status': 'processing', 'message': 'Creating high level demo flow'})}\n\n"
        create_steps_prompt(context)

        yield f"data: {json.dumps({'status': 'processing', 'message': 'Generating demo video'})}\n\n"
        context['start_url'] = 'https://elevenlabs.io/app/home'
        asyncio.run(gen_video(context))

        process_logs(context)

        yield f"data: {json.dumps({'status': 'processing', 'message': 'Generating transcript for demo'})}\n\n"
        gen_transcript(context)

        yield f"data: {json.dumps({'status': 'processing', 'message': 'Converting transcript audio into audio of your preferred lanaguage'})}\n\n"
        gen_audio(context)

        merge_video_audio(context)

        final_video_path = context.get('final_video_path')
        yield f"data: {json.dumps({'status': 'success', 'request_id': request_id, 'final_video_path': final_video_path})}\n\n"

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"

@app.route('/generate', methods=['GET'])
def run():
    return Response(stream_with_context(handle_generate()), mimetype='text/event-stream')
    
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

if __name__ == '__main__':
    app.run(debug=True, port=5001)