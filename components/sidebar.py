import os
import tempfile
import requests
import streamlit as st

ALLOWED_EXTENSIONS = [".pdf", ".docx", ".doc", ".txt", ".ppt", ".csv", ".html", ".xls"]


def get_saved_files_info():
    return []


def is_allowed_extension(file_name):
    return os.path.splitext(file_name)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(uploaded_file):
    if is_allowed_extension(uploaded_file.name):
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
        ) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            st.toast(
                f"O arquivo {uploaded_file.name} foi salvo no armazenamento temporário."
            )
            return temp_file.name, os.path.splitext(uploaded_file.name)[1].lower()
    else:
        st.error("Formato de arquivo não suportado.", icon="🚨")


def upload_file_via_url(url):
    try:
        response = requests.get(url)
        file_ext = os.path.splitext(url)[1].lower()
        if response.status_code == 200 and file_ext in ALLOWED_EXTENSIONS:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=file_ext
            ) as temp_file:
                temp_file.write(response.content)
                st.toast(f"Documento salvo da URL para armazenamento temporário.")
                return temp_file.name, file_ext
        else:
            st.error("URL inválida ou tipo de conteúdo não suportado.", icon="🚨")
    except requests.RequestException as e:
        st.error("Falha ao buscar documento da URL.", icon="🚨")


def sidebar():
    saved_files_info = get_saved_files_info()
    with st.sidebar:
        documents_uploads = st.file_uploader(
            "Carregar documentos",
            accept_multiple_files=True,
        )
        if documents_uploads:
            for uploaded_file in documents_uploads:
                file_info = save_uploaded_file(uploaded_file)
                if file_info:
                    saved_files_info.append(file_info)

        st.markdown("***")

        documents_uploads_url = st.text_input(
            "Carregar documentos via url",
        )
        submit_button = st.button("Link para upload")
        if submit_button and documents_uploads_url:
            file_info = upload_file_via_url(documents_uploads_url)
            if file_info:
                saved_files_info.append(file_info)

        st.markdown("***")

        with st.expander("Credenciais"):
            openai_keys = st.text_input(
                "Chave API OpenAI", type="password", value=os.environ["OPENAI_API_KEY"]
            )

        st.markdown("***")
        complete_button = st.button(
            "Configuração completa", disabled=not (saved_files_info and openai_keys)
        )

        if complete_button:
            return saved_files_info, openai_keys
        else:
            return None, None
