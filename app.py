import streamlit as st
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Loading the environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuring the api key...
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are the YouTube video summarizer. You will take the transcript text and will summarize the entire video and provide the important summary in points within 250 words. The transcript text is given here : """

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        video_id = video_id.split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        # The transcript_text will be in the form of a list. So we will iterate through each element.
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e

## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([transcript_text + prompt])
    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    video_id = video_id.split("&")[0]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
