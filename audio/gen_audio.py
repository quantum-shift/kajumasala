import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def gen_audio_internal(request_id, text, voice_id, voice_settings):
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2",
        # voice_settings=voice_settings,
    )

    audio_path = f"./audio/audio_{request_id}.mp3"
    with open(audio_path, "wb") as file:
        for chunk in audio:
            if chunk:
                file.write(chunk)
    return audio_path

def gen_audio(context: dict):
    if not context.get('transcript'):
        raise RuntimeError("Missing transcript in gen_audio")
    if not context.get('request_id'):
        raise RuntimeError("Missing request_id in gen_audio")
    
    request_id = context.get('request_id')
    transcript = context.get('transcript')
    voice_id = "JBFqnCBsd6RMkjVDRZzb"
    voice_settings = {}
    
    audio_path = gen_audio_internal(request_id, transcript, voice_id, voice_settings)
    context['audio_path'] = audio_path
    

if __name__ == "__main__":
    text = ""
    with open("./audio/transcript/transcript.txt", "r") as file:
        text = file.read()
    language = "en"
    voice_id = "JBFqnCBsd6RMkjVDRZzb"
    voice_settings = {}
    audio = gen_audio('test_request_id', text, voice_id, voice_settings)
