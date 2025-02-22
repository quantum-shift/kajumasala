import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def gen_audio(text, language, voice_id, voice_settings):
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        # language_code=language,
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2",
        # voice_settings=voice_settings,
    )
    with open("./audio/audio.mp3", "wb") as file:
        for chunk in audio:
            if chunk:
                file.write(chunk)

if __name__ == "__main__":
    text = ""
    with open("./audio/transcript/transcript.txt", "r") as file:
        text = file.read()
    language = "en"
    voice_id = "JBFqnCBsd6RMkjVDRZzb"
    voice_settings = {}
    audio = gen_audio(text, language, voice_id, voice_settings)
