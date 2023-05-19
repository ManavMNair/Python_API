from flask import Flask, request, jsonify
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re


app = Flask(__name__)


@app.route('/get-summary', methods=['POST'])

def get_video_id():
    youtube_video = request.json.get('youtube_video')
    if '=' in youtube_video:
        video_id = youtube_video.split("=")[1]
        print("video id ="+video_id)
        Final_summary=get_summary(video_id,youtube_video)
        return (Final_summary)
    else:
        return jsonify(error='Invalid YouTube URL')  


def get_summary(video_id,youtube_video):
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if transcript:
              # ===============If transcript of the video available ============
            print("Transcript fetched successfully") 
            result=""
            for i in transcript:
                result+=' '+i['text']

            # print(len(result))

            summarizer = pipeline('summarization')
            print("Summarisation started")

            num_iters = int(len(result)/1000)
            summarized_text = []
            for i in range(0, num_iters + 1):
                start = 0
                start = i * 1000
                end = (i + 1) * 1000
                # print("input text \n" + result[start:end])
                max_length = min(150, len(result[start:end]))
                out = summarizer(result[start:end], max_length=max_length)
                out = out[0]
                out = out['summary_text']
                percentage = (((i+1)/num_iters)*100)
                print("Summarized "+str(percentage) +"%")
                summarized_text.append(out)

                summary=str(summarized_text)
                cleaned_summary = re.sub(r'[\"]', '', summary)
            return jsonify(summary=cleaned_summary)
        else:  # ========================if transcript not available====================
            from pytube import YouTube
            import speech_recognition as sr
            from os import path
            import subprocess
            import ffmpeg
            import os
            # Initialize the recognizer
            r = sr.Recognizer()



            
            yt = YouTube(youtube_video)
            # FOR CONSOLE ONLY 
            print("Download starred")
            # ======FOR CONSOLE ONLY======== 
            

            
            yt.streams\
                .filter(only_audio=True,file_extension='mp4')\
                    .first()\
                        .download(filename='ytaudio.mp4')
            print("file downloaded ")
            input_file = 'ytaudio.mp4'
            output_file = 'ytaudio.wav'
            if os.path.exists(output_file):
                os.remove(output_file)

            command = [
                'ffmpeg',
                '-i', 'ytaudio.mp4',
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                'ytaudio.wav'
            ]

            try:
                subprocess.call(command, shell = True)
                print("converted")
            except subprocess.CalledProcessError as e:
                print("conversion failed, error: ",e)


            # Read the audio file
            with sr.AudioFile(output_file) as source:
                # Load audio data into the recognizer
                audio_data = r.record(source)
                transcript = []
                
                # Perform the speech recognition
                transcript = r.recognize_google(audio_data)

            
                result=""
                for i in transcript:
                    result+=' '+i['text']

                # print(len(result))

                summarizer = pipeline('summarization')

                num_iters = int(len(result)/1000)
                summarized_text = []
                for i in range(0, num_iters + 1):
                    start = 0
                    start = i * 1000
                    end = (i + 1) * 1000
                    # print("input text \n" + result[start:end])
                    max_length = min(150, len(result[start:end]))
                    out = summarizer(result[start:end], max_length=max_length)

                    out = out[0]
                    out = out['summary_text']
                    percentage = (((i+1)/num_iters)*100)
                    print("Summarized "+str(percentage)+"%")
                    summarized_text.append(out)

                    summary=str(summarized_text)
                    cleaned_summary = re.sub(r'[\"]', '', summary)
            return jsonify(summary=cleaned_summary)

    except Exception as e:
        return jsonify(error="An error occurred:" + str(e))
        #==========================Function ends================

   
if __name__ == '__main__':

    app.run(debug=True)