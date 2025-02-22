from flask import Flask, request, jsonify, Response
import logging
from generateDemoSteps import create_steps_prompt, explore_web_app
from audio import gen_audio, gen_transcript, crawl
from generateDemoVideo import generateDemoVideo as gen_video
from generateAppFeatures import exploreAppBrowserUse as explore_app
from audio.process_logs import process_logs
from overlay.merge_av import merge_video_audio
import uuid
import traceback
import asyncio
from flask_cors import CORS


import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# def gen_video(context):
#     logging.info("Generating video")
#     pass

@app.route('/generate', methods=['POST'])
def run():
    try:
        user_query = request.json.get('user_query')
        language = request.json.get('language')
        if not user_query or not language:
            return jsonify({'status': 'error', 'message': 'Missing required data'}), 400
        
        request_id = uuid.uuid4()

        context = {'user_query': user_query, 'request_id': request_id, 'language': language}
        context['start_url'] = 'https://elevenlabs.io/app/home'
        logging.info(f"Received user query: {user_query}")
        # crawl(context)

        # browser use to explore the web app first
        explore_web_app(context)
        asyncio.run(explore_app(context))

        get_app_feature_from_user_query(context, user_query)
        # based on user query, create steps prompt
        create_steps_prompt(context)
        


        asyncio.run(gen_video(context))

        print(context['app_features'])
        print('KB: here')

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
    
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res
    
def get_app_feature_from_user_query(context, user_query):
    app_features = context['explore_app_features']
    llm_prompt = ""
    # read from map
    with open("mapQueryToFeature.prompt", "r") as file:
        app_feature_query = file.read()
    app_feature_llm_query = app_feature_query.format(features=app_features, user_query=user_query)
    print(app_feature_llm_query)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": app_feature_llm_query
            },
        ],
        store=True
    )

    context['app_feature'] = completion.choices[0].message.content
    print("app_feature: UD")
    print(context['app_feature'])

if __name__ == '__main__':
    app.run(debug=True, port=5001)