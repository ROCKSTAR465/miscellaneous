import streamlit as st
import whisper
import os
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def main():
    st.set_page_config(page_title="SubNXT", page_icon="🎥", layout="wide")

    # Navbar
    st.markdown("""
    <style>
    nav { position: fixed; top: 0; left: 0; width: 100%; background-color: #0e1117; z-index: 1000; }
    nav a { color: #f63366; margin: 0 1rem; text-decoration: none; font-size: 1.2rem; }
    </style>
    <nav><a href="/">Home</a> <a href="#features">Features</a></nav>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 4rem 0; background-color: #f63366; color: white;">
        <h1>Welcome to SubNXT</h1>
        <p>Generate professional subtitles from your videos in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    # Lottie Animation
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_ynz8y3ds.json"
    st_lottie(load_lottie_url(lottie_url), height=300, key="lottie-animation")

    # Features Section
    st.markdown("""
    <div class="card">🎥 <h2>Upload Videos</h2><p>Upload MP4 videos easily.</p></div>
    """, unsafe_allow_html=True)

    # File Upload
    uploaded_file = st.file_uploader("Upload a video", type=["mp4"])
    if uploaded_file:
        st.write("Processing video...")
        # Add Whisper logic here

if __name__ == "__main__":
    main()
