import streamlit as st


@st.dialog("Conexão com Banco de Dados!")
def future_feature():
    message = (
        "A funcionalidade de conexão com banco de dados ainda não está disponível."
    )
    st.write(message)


@st.dialog("Resposta com voz")
def audio_feature():
    default_value = st.session_state.get("enable_audio", True)
    st.write(
        "Quando habilitado, transcreve a resposta textual do chatbot para áudio e inicia a reprodução do áudio automáticamente."
    )
    value = st.checkbox(
        label="Habilita Àudio",
        value=default_value,
    )
    st.session_state["enable_audio"] = value
