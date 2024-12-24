import openai
import streamlit as st
import soundfile as sf
import whisper

# # Set your OpenAI API key
# openai.api_key = st.secrets["my_key"]


def transcribe_audio(audio_file, languages):
    """
    Transcribes audio using the OpenAI Whisper API, supporting multiple languages.

    Args:
    audio_file: The audio file to transcribe.
    languages: A list of language codes.

    Returns:
    The transcribed text.
    """
    try:
        with open(audio_file, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f, language=languages)
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

# Streamlit app
st.title("Audio Transcription and Translation")

# Terms and Conditions
st.markdown(
    """
    **Terms and Conditions**

    This application is provided for educational and research purposes only. 
    By using this application, you agree to the following:

    * You are solely responsible for any and all use of this application.
    * You will not use this application for any unauthorized or illegal purposes.
    * The developers of this application are not liable for any damages or losses arising from your use of this application.
    * This application is provided "as is" without any warranties, express or implied.
    * The audio transcription feature utilizes artificial intelligence, which may produce inaccurate results. You are responsible for reviewing and verifying the accuracy of any transcriptions.

    Please read these terms and conditions carefully before using this application.
    """
)

# Agreement checkbox
if st.checkbox("I agree to the Terms and Conditions"):
    uploaded_files = st.file_uploader("Upload audio files", type=["ogg", "wav", "mp3", "opus"], accept_multiple_files=True)

    # Get language names and codes from whisper.tokenizer.LANGUAGES
    language_options = list(whisper.tokenizer.LANGUAGES.items())

    # Allow multiple language selection
    selected_languages = st.multiselect(
        "Select audio language(s)", 
        [lang[1] for lang in language_options]
    )

    # Get corresponding language codes
    audio_language_codes = [
        lang[0] for lang in language_options if lang[1] in selected_languages
    ]

    target_language = st.selectbox("Select target language", ["English", "French", "Spanish", "German", "Chinese"])

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded file temporarily
            with open("temp_audio.ogg", "wb") as f:
                f.write(uploaded_file.read())

            # Transcribe the audio with multiple languages
            with st.spinner(f"Transcribing {uploaded_file.name}..."):
                transcription = transcribe_audio("temp_audio.ogg", audio_language_codes)
            st.write(f"**Transcription of {uploaded_file.name}:**", transcription)

            # Translate the text
            with st.spinner("Translating text..."):
                translation = translate_text(transcription, target_language)
            st.write("**Translation:**", translation)

else:
    st.warning("Please accept the Terms and Conditions to proceed.")


# def transcribe_audio(audio_file, languages):
#     """
#     Transcribes audio using the OpenAI Whisper API, supporting multiple languages.

#     Args:
#     audio_file: The audio file to transcribe.
#     languages: A list of language codes.

#     Returns:
#     The transcribed text.
#     """
#     try:
#         with open(audio_file, "rb") as f:
#             transcript = openai.Audio.transcribe("whisper-1", f, language=languages)
#         return transcript.text
#     except Exception as e:
#         return f"Error transcribing audio: {e}"

# def translate_text(text, target_language):
#     """
#     Translates text using the OpenAI API.

#     Args:
#     text: The text to translate.
#     target_language: The target language.

#     Returns:
#     The translated text.
#     """
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that translates text."},
#                 {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
#             ]
#         )
#         return response.choices[0].message['content']
#     except Exception as e:
#         return f"Error translating text: {e}"



# # Streamlit app
# st.title("Audio Transcription and Translation")

# # Terms and Conditions
# st.markdown(
#     """
#     **Terms and Conditions**

#     This application is provided for educational and research purposes only. 
#     By using this application, you agree to the following:

#     * You are solely responsible for any and all use of this application.
#     * You will not use this application for any unauthorized or illegal purposes.
#     * The developers of this application are not liable for any damages or losses arising from your use of this application.
#     * This application is provided "as is" without any warranties, express or implied.
#     * The audio transcription feature utilizes artificial intelligence, which may produce inaccurate results. You are responsible for reviewing and verifying the accuracy of any transcriptions.

#     Please read these terms and conditions carefully before using this application.
#     """
# )

# # Agreement checkbox
# if st.checkbox("I agree to the Terms and Conditions"):
#     uploaded_file = st.file_uploader("Upload an audio file", type=["ogg", "wav", "mp3", "opus"])

#     # Get language names and codes from whisper.tokenizer.LANGUAGES
#     language_options = list(whisper.tokenizer.LANGUAGES.items())

#     # Allow multiple language selection
#     selected_languages = st.multiselect(
#         "Select audio language(s)", 
#         [lang[1] for lang in language_options]
#     )

#     # Get corresponding language codes
#     audio_language_codes = [
#         lang[0] for lang in language_options if lang[1] in selected_languages
#     ]

#     target_language = st.selectbox("Select target language", ["English", "French", "Spanish", "German", "Chinese"])

#     if uploaded_file is not None:
#         # Save the uploaded file temporarily
#         with open("temp_audio.ogg", "wb") as f:
#             f.write(uploaded_file.read())

#         # Transcribe the audio with multiple languages
#         with st.spinner("Transcribing audio..."):
#             transcription = transcribe_audio("temp_audio.ogg", audio_language_codes)
#         st.write("Transcription:", transcription)

#         # Translate the text
#         with st.spinner("Translating text..."):
#             translation = translate_text(transcription, target_language)
#         st.write("Translation:", translation)


else:
    st.warning("Please accept the Terms and Conditions to proceed.")


