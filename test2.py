import pyttsx3
import streamlit as st
import langdetect

# Initialize session state to store speak_called flag
if 'speak_called' not in st.session_state:
    st.session_state.speak_called = False

def detect_language(text):
    try:
        # Detect the language of the text
        lang = langdetect.detect(text)
        return lang
    except:
        # Return None if language detection fails
        return None

def get_voice_id(language):
    # Check the detected language and return voice ID accordingly
    if language == 'en':
        # Return the ID for English voice
        return 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    elif language == 'mr':
        # Return the ID for Marathi voice
        return 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_MARATHI_MADHAV_11.0'
    else:
        # Return None for unsupported languages
        return None

def speak(text):
    if text:
        # Detect the language of the input text
        language = detect_language(text)
        if language:
            # Get the voice ID based on the detected language
            voice_id = get_voice_id(language)
            if voice_id:
                # Initialize the pyttsx3 engine
                engine = pyttsx3.init()
                # Set the voice by ID
                engine.setProperty('voice', voice_id)
                # Set the speaking rate (optional)
                engine.setProperty('rate', 150)
                # Speak the text
                engine.say(text)
                engine.runAndWait()
            else:
                st.error("Voice not available for the detected language.")
        else:
            st.error("Language detection failed.")
    else:
        st.subheader("")

# Example usage:
text_to_speak = "नमस्ते, मी LUFFY आहे, मी तुम्हाला कसे मदत करू शकतो?"
# Check if the function has not been called before
if not st.session_state.speak_called:
    speak(text_to_speak)
    # Set the flag to indicate that the function has been called
    st.session_state.speak_called = True
