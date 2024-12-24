import openai
import streamlit as st
import soundfile as sf
import whisper

# Set your OpenAI API key
openai.api_key = st.secrets["my_key"]

def transcribe_audio(audio_file, language):
    """
    Transcribes audio using the OpenAI Whisper API.

    Args:
    audio_file: The audio file to transcribe.
    language: The language of the audio.

    Returns:
    The transcribed text.
    """
    try:
        with open(audio_file, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f, language=language)
        return transcript.text
    except Exception as e:
        return f"Error transcribing audio: {e}"

def translate_text(text, target_language):
    """
    Translates text using the OpenAI API.

    Args:
    text: The text to translate.
    target_language: The target language.

    Returns:
    The translated text.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates text."},
                {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error translating text: {e}"

def analyze_sentiment(text):
    """
    Analyzes the sentiment of text using the OpenAI API.

    Args:
    text: The text to analyze.

    Returns:
    The sentiment of the text.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes sentiment."},
                {"role": "user", "content": f"Analyze the sentiment of the following text: {text}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error analyzing sentiment: {e}"

# Streamlit app
st.title("Audio Transcription and Translation")

uploaded_file = st.file_uploader("Upload an audio file", type=["ogg", "wav", "mp3"])
audio_language = st.selectbox("Select audio language", list(whisper.tokenizer.LANGUAGES.keys()))
target_language = st.selectbox("Select target language", ["English", "French", "Spanish", "German", "Chinese"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("temp_audio.ogg", "wb") as f:
        f.write(uploaded_file.read())

    # Transcribe the audio
    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio("temp_audio.ogg", audio_language)
    st.write("Transcription:", transcription)

    # Translate the text
    with st.spinner("Translating text..."):
        translation = translate_text(transcription, target_language)
    st.write("Translation:", translation)

    # Analyze sentiment
    with st.spinner("Analyzing sentiment..."):
        sentiment = analyze_sentiment(transcription)
    st.write("Sentiment:", sentiment)
