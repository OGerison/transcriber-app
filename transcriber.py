import os
import speech_recognition as sr
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

def convert_wav_to_text(wav_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {e}"

def main():
    input = "E:/Transcriber/inputs/"
    output = "E:/Transcriber/outputs/"

    for mp3_file in os.listdir(input):
        wav_file = "temp.wav"
        txt_output_file = os.path.join(output, mp3_file[:-4] + ".txt")

        convert_mp3_to_wav(os.path.join(input, mp3_file), wav_file)
        text = convert_wav_to_text(wav_file)

        with open(txt_output_file, "w") as txt_file:
            txt_file.write(text)

        os.remove(wav_file)  # Remove the temporary WAV file
        print("Conversion complete. Text saved to", txt_output_file)

if __name__ == "__main__":
    main()