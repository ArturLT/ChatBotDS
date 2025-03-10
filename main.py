import os
import json
import streamlit as st
import google.generativeai as genai

# Configuração da chave da API do Gemini
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GEMINI_API_KEY = config_data["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)  # Configura a API do Gemini

# Configuração do Streamlit
st.set_page_config(
    page_title="ChatBot Dark Souls",
    page_icon="⚜️",
    layout="centered",
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tema Dark Souls - Prompt de Instrução
prompt_sistema = """
Você é um especialista no jogo Dark Souls e sabe tudo sobre a lore, personagens, estratégias, mapas, e segredos do jogo. 
Responda às perguntas de maneira precisa e dentro do contexto do universo de Dark Souls.
Quando alguém perguntar sobre o jogo, forneça detalhes e dicas relevantes, sempre mantendo o estilo e a atmosfera sombria e misteriosa do jogo.
"""

st.title("🔥 ChatBot Dark Souls")

st.markdown("""
**Bem-vindo ao ChatBot Dark Souls!**

Sou um especialista no universo de **Dark Souls**, um jogo desafiador e repleto de mistérios. 
Aqui, você pode me perguntar tudo sobre a lore, personagens, armas, estratégias de combate e segredos escondidos.
Meu objetivo é guiá-lo nesse mundo sombrio e complexo, oferecendo dicas e informações valiosas sobre o jogo.
Quando você estiver pronto, basta digitar sua pergunta e eu responderei com o máximo de detalhes que eu souber!
""")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Fale com o ChatBot sobre Dark Souls...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Combina o prompt do sistema com o prompt do usuário
    combined_prompt = prompt_sistema + "\n" + "Pergunta do usuário: " + user_prompt

    model = genai.GenerativeModel("models/gemini-1.5-pro")  # Escolhe o modelo do Gemini
    response = model.generate_content(combined_prompt)  # Passa o prompt combinado

    assistant_response = response.text  # Obtém a resposta do Gemini
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
