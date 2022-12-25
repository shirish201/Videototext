

import whisper
from whisper.utils import write_vtt
# import ffmpeg
import pandas as pd
import os
import sys
import subprocess
import torch 
from whisper.model import Whisper, ModelDimensions
import streamlit as st
import time
import moviepy
from moviepy.editor import *
import tempfile

## Upload the video File and convert to mp3

@st.cache(persist=True,allow_output_mutation=False,show_spinner=True,suppress_st_warning=True)
def video2mp3(video_file, output_ext="mp3"):
    print("here1")
    videoclip = VideoFileClip(video_file)
    audioclip = videoclip.audio
    temp_file_2 = tempfile.mkstemp(suffix='.mp3')
    print(temp_file_2[1])
    audioclip.write_audiofile(temp_file_2[1])
    return temp_file_2[1]
    

@st.cache(persist=True,allow_output_mutation=False,show_spinner=True,suppress_st_warning=True)
def process_audio(filename):
    #checkpoint = torch.load("Model_Small/small.pt")
    #dims = ModelDimensions(**checkpoint["dims"])
    #model = Whisper(dims)
    print("here")
    #model.load_state_dict(checkpoint["model_state_dict"])
    
    model = whisper.load_model("small")
    #### Run transcribe
    result = model.transcribe(filename)
    print(result["text"])
 
    return result


def main():
    # Streamlit configx`
    st.set_page_config(
        page_title="YouTube Video Transcription with Whisper",
        layout="centered",
    )
    
    uploaded_file = st.file_uploader("Choose a file", type=["mp4", "mpeg"])
    if uploaded_file is not None:
        file_details = {"Filename":uploaded_file.name, "FileType":uploaded_file.type}
        st.write(file_details)
        
        temp_file_1 = tempfile.mkstemp(suffix='.mp4')
        with open(os.path.join(temp_file_1[1]),"wb") as f:
            f.write(uploaded_file.getbuffer())
        
        
        audio_file = video2mp3(video_file = temp_file_1[1])
        
        print(audio_file)
    
        ### Load the whisper model
        if st.button("Generate Transcript"):
            with st.spinner(f"Generating Transcript... 💫"):
                result = process_audio(filename = audio_file)
                data_subtitle = pd.DataFrame()
                for i in range(len(result["segments"])):
                  data_subtitle.loc[i, "id"] = i
                  data_subtitle.loc[i, "start"] = result["segments"][i]["start"]
                  data_subtitle.loc[i, "end"] = result["segments"][i]["end"]
                  data_subtitle.loc[i, "text"] = result["segments"][i]["text"]
                  
                temp_file_vtt = tempfile.mkstemp(suffix='.vtt')
                with open(temp_file_vtt[1], "w") as vtt:
                    write_vtt(result["segments"], file=vtt)
                
                ### Save VTT file
                # subtitle = temp_file_2[1]
                # output_video = ('Output/'+input_video.split(".")[0]).replace("/Raw","") + "_subtitled_today"
                
                # temp_file_3 = tempfile.mkstemp(suffix='.mp4')
                # print(temp_file_3[1])

                temp_file_10 = tempfile.mkstemp(suffix='.mp4')
                
                ### Output the video file
                os.system(f"""
                ffmpeg -i {temp_file_1[1]} -y {temp_file_10[1]},
                """)
                with open(temp_file_10[1]) as f:
                    st.download_button('Download video', f)  # Defaults to 'text/plain'
                    
                if temp_file_10[1] is not None:
                    video_file = open(temp_file_10[1], 'rb')
                    video_bytes = video_file.read()
                    st.video(video_bytes)
                 
                    
                
        # if temp_file_1[1] is not None:
        # ### Output the video file
              
        #     os.system(f"""
        #     ffmpeg -i {temp_file_1[1]}  -y {temp_file_10[1]}
        #     """)
            
                

main()
