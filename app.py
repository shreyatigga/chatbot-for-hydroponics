import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

st.set_page_config(page_title="Hydroponics", page_icon=":seedling:")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain

names = ["Aman Dev", "Shreya Tigga", "Sowmiya", "Employee"]
usernames = ["aman", "shreya", "sowmiya", "vtu19464"]
# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "minor2",
    "abcdef",
)
name, authentication_status, username = authenticator.login("Login", "sidebar")
identity = username[0:3]


def main():
    load_dotenv()
    st.write(css, unsafe_allow_html=True)
    if authentication_status:
        st.success(f"Welcome, {username}!")
        authenticator.logout("Logout", "main")

    def handle_userinput(user_question):
        response = st.session_state.conversation({"question": user_question})

        st.session_state.chat_history = response["chat_history"]
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(
                    user_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )
            else:
                st.write(
                    bot_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat-Bot for Hydroponics 🌱")
    user_question = st.text_input(
        "Ask me anything about hydroponics:",
        key="unique_key_for_normal_question",
    )
    if user_question:
        handle_userinput(user_question)
    file_paths = [
        "C:\\Users\\USER\\Desktop\\Work\\study\\3rd year\\6th sem\\Minor 2\\chatbot for hydroponics\\User Manual.pdf",
        "C:\\Users\\USER\\Desktop\\Work\\study\\3rd year\\6th sem\\Minor 2\\chatbot for hydroponics\\Hydroponic_vegetable_cultivation.pdf",
    ]
    for file_path in file_paths:
        pdf_docs = open(file_path, "rb")

    raw_text = get_pdf_text([pdf_docs])

    text_chunks = get_text_chunks(raw_text)

    vectorstore = get_vectorstore(text_chunks)

    st.session_state.conversation = get_conversation_chain(vectorstore)
    if authentication_status == False:
        st.sidebar.error("Username/password is incorrect")
    if authentication_status == None:
        st.sidebar.warning("Please enter your username and password")


if __name__ == "__main__":
    main()
