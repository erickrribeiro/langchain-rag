import streamlit as st


@st.dialog("Conexão com Banco de Dados!")
def future_feature():
    with st.form("db_form"):
        st.selectbox(
            label="Dialect",
            options=["PostgreSQL", "MySQL", "Databricks", "Customizado"],
        )
        st.text_input(label="Descrição")
        col1, col2 = st.columns(spec=[0.8, 0.2])
        with col1:
            st.text_input(label="Host", placeholder="127.0.0.1")
        with col2:
            st.text_input(label="Port", placeholder="5432")

        st.text_input(label="Usuário")
        st.text_input(label="Senha", type="password")

        st.form_submit_button("Conectar")


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
