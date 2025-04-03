import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, ChatPromptTemplate
)

# WhatsApp-style CSS with black text for chat history
st.markdown("""
    <style>
        .chat-container {
            max-width: 600px;
            margin: auto;
            padding: 10px;
        }
        .user-message {
            background-color: #dcf8c6;
            color: black;  /* Set text color to black */
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: right;
            display: inline-block;
            width: fit-content;
            max-width: 80%;
        }
        .assistant-message {
            background-color: #ffffff;
            color: black;  /* Set text color to black */
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: left;
            display: inline-block;
            width: fit-content;
            max-width: 80%;
        }
        .message-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 5px;
            margin-bottom: 10px;
        }
        .user-container {
            align-items: flex-end !important;
        }
        /* JavaScript for Enter key functionality */
        .stTextInput textarea {
            width: 100%;
            padding: 10px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit Title
st.title("💬 MAN.AI")
st.caption("👨‍💻 **Developer:** MD AIMAN ALI SHEZAN")

# Initialize LLM Model
llm_model = ChatOllama(model="CognitiveComputations/dolphin-llama3.1")
system_message = SystemMessagePromptTemplate.from_template(
    "You are a helpful AI Assistant. if you find any question related to who is your creator  then reply Sir Ai-Man and if you find any question like what is your name then reply Man.Ai . "
)

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Input Form
with st.form("chat-form", clear_on_submit=True):
    text = st.text_area("💬 Type your message...", key="user_input")
    submit = st.form_submit_button("Send")

# Function to Generate Response
def generate_response(chat_history):
    chat_template = ChatPromptTemplate.from_messages(chat_history)
    chain = chat_template | llm_model | StrOutputParser()
    response = chain.invoke({})
    return response

# Retrieve Chat History
def get_history():
    chat_history = [system_message]
    for chat in st.session_state['chat_history']:
        chat_history.append(HumanMessagePromptTemplate.from_template(chat['user']))
        chat_history.append(AIMessagePromptTemplate.from_template(chat['assistant']))
    return chat_history

# JavaScript to handle the Enter key and trigger the submit button (auto-send on Enter)
st.markdown("""
    <script>
        document.querySelector('textarea').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();  // Prevent default Enter behavior (new line)
                document.querySelector('button[type=submit]').click();  // Simulate the submit button click
            }
        });
    </script>
""", unsafe_allow_html=True)

# Process User Input
if submit and text:
    with st.spinner("Thinking... 🤖"):
        chat_history = get_history()
        chat_history.append(HumanMessagePromptTemplate.from_template(text))
        response = generate_response(chat_history)

        # Save Chat to History
        st.session_state['chat_history'].append({'user': text, 'assistant': response})

# Display Chat History
st.markdown("### 🗨️ Chat History")

for chat in reversed(st.session_state["chat_history"]):
    st.markdown(
        f'<div class="message-container user-container">'
        f'<div class="user-message">👤 {chat["user"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="message-container">'
        f'<div class="assistant-message">🤖 {chat["assistant"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
