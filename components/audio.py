import base64

import streamlit as st
from openai import OpenAI


def autoplay_audio3(message: str) -> None:
    file_path = text_to_speech(message)

    with open(file_path, mode="rb") as reader:
        b64 = base64.b64encode(reader.read()).decode()
        if st.session_state.get("enable_audio", False):
            md = f"""
                <audio id="audioTag" controls autoplay>
                <source src="data:audio/mp3;base64,{b64}"  type="audio/mpeg" format="audio/mpeg">
                </audio>
                """
        else:
            md = f"""
                <audio id="audioTag" controls>
                <source src="data:audio/mp3;base64,{b64}"  type="audio/mpeg" format="audio/mpeg">
                </audio>
                """
    st.markdown(
        md,
        unsafe_allow_html=True,
    )


def text_to_speech(text: str) -> str:
    target = "audio.mp3"
    client = OpenAI()
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file(target)

    return target
