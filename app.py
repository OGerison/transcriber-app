import os
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment

# Set a longer timeout for the Streamlit app
#st.set_option('server.maxUploadSize', 1000)  # Adjust the value as needed

def convert_mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

def convert_wav_to_text(wav_file, segment_duration=15):
    recognizer = sr.Recognizer()
    audio_text = []

    sound = AudioSegment.from_wav(wav_file)
    total_duration = len(sound)

    for start_time in range(0, total_duration, segment_duration * 1000):
        end_time = start_time + segment_duration * 1000
        segment = sound[start_time:end_time]

        with sr.AudioFile(segment.export(format="wav")) as source:
            audio = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio, show_all=False)
                audio_text.append(text)
            except sr.UnknownValueError:
                audio_text.append("Could not understand audio")
            except sr.RequestError as e:
                audio_text.append(f"Error: {e}")

    return "\n".join(audio_text)

def main():
    st.title("Audio to Text Transcriber")

    uploaded_file = st.file_uploader("Upload an audio file (MP3)", type=["mp3"])
    
    if uploaded_file is not None:
        wav_file = "temp.wav"
        convert_mp3_to_wav(uploaded_file, wav_file)
        text = convert_wav_to_text(wav_file, segment_duration=15)
        st.text("Transcription:")
        st.write(text)
        
        # Get the output directory path
        output_dir = "E:\Transcriber\outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create the output text file path
        txt_output_file = os.path.join(output_dir, uploaded_file.name[:-4] + ".txt")
        
        with open(txt_output_file, "w") as txt_file:
            txt_file.write(text)

        st.download_button("Download Text", txt_output_file)

        os.remove(wav_file)

if __name__ == "__main__":
    main()
