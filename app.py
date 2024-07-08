import openai
import streamlit as st

from components.audio import autoplay_audio3
from components.sidebar import sidebar
from components.utils import initialize_state, load_qa_chain


def main():
    # Set up the Streamlit page configuration and title
    st.set_page_config(page_title="Chat Diebold (Privacy Security)")
    st.markdown("""
        <style>
        .icon {
            position: fixed;
            # bottom: 10px;
            right: 10px;
            font-size: 40px;
            color: #007BFF;
        }
        </style>
        """, unsafe_allow_html=True)

    # Include the Font Awesome script and the icon
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
        <i class="fas fa-database icon"></i>
        """, unsafe_allow_html=True)

    # Display the main content
    # st.image('./assets/officedatabase_104402.png')
    col1, col2 = st.columns(spec=[0.4, 0.6])

    with col1:
        st.image("./assets/robot.png", width=150)

    with col2:
        st.title("Um Chatbot que lê documentos")

    # Invoke the sidebar for user inputs like file uploads and OpenAI keys
    saved_files_info, openai_keys = sidebar()
    st.markdown("***")
    st.subheader("Interação com documentos")

    # Initialize the session state variables
    initialize_state()

    # Add a flag in the session state for API key validation
    if "is_api_key_valid" not in st.session_state:
        st.session_state.is_api_key_valid = None

    # Load the QA chain if documents and OpenAI keys are provided, and handle OpenAI AuthenticationError
    if saved_files_info and openai_keys and not st.session_state.qa_chain:
        try:
            st.session_state.qa_chain = load_qa_chain(saved_files_info, openai_keys)
            st.session_state.is_api_key_valid = True  # Valid API key
        except openai.AuthenticationError as e:
            st.error(
                'Forneça uma chave de API válida. Atualize a chave de API na barra lateral e clique em "Concluir configuração" para prosseguir.',
                icon="🚨",
            )
            st.session_state.is_api_key_valid = False  # Invalid API key

    # Enable the chat section if the QA chain is loaded and API key is valid
    if st.session_state.qa_chain and st.session_state.is_api_key_valid:
        st.success("Configuração concluída")
        prompt = st.chat_input(
            "Faça perguntas sobre os documentos enviados", key="chat_input"
        )

        # Process user prompts and generate responses
        if prompt and (
                st.session_state.messages[-1]["content"] != prompt
                or st.session_state.messages[-1]["role"] != "user"
        ):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner(
                    "Recuperando informações relevantes e gerando resultados..."
            ):
                response = st.session_state.qa_chain.run(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Display the conversation messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        last_message = st.session_state.messages[-1]["content"]
        autoplay_audio3(last_message)
    else:
        st.info("Conclua a configuração na barra lateral para prosseguir.")
        # Disable the chat input if the API key is invalid
        no_prompt = st.chat_input(
            "Faça perguntas sobre os documentos enviados",
            disabled=not st.session_state.is_api_key_valid,
        )


if __name__ == "__main__":
    main()
