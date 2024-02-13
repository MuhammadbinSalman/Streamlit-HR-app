import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import time
from openai.types.chat.chat_completion import ChatCompletion
from API_calling import *


_ : bool = load_dotenv(find_dotenv()) # read local .env file
client : OpenAI = OpenAI()

st.title("CV pdf analyzer")
st.sidebar.title("Configuration")
entered_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
st.markdown("""
       Use this AI tool to analyze cvs and get your required candidates. Ideal for:
        - :page_facing_up: **Businesses** to get the right candidate who meets their requirements.
        - :mag_right: **Hiring teams** to have an AI assistant which can help them in their tasks.
        - :clipboard: Indivisuals **to get their cvs analyzed and further tips** to make their cvs even better.

        Upload a PDF file and enter your specific query related to the about what kind of candidate you are looking for.
    """)
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"],
                                  accept_multiple_files=True
                                 )
user_query = st.text_input("Enter your query about the PDF:")
def pretty_print(messages):
    responses = []
    for m in messages:
        if m.role == "assistant":
            responses.append(m.content[0].text.value)
    return "\n".join(responses)
assistant: Assistant = client.beta.assistants.create(
    name="HR support assistant",
    instructions="You are a helpful AI assistant for HR team, you're designed to streamline user's CV filtering process effortlessly. You will be provided with the relevant PDFs of candidate's CVs and a text in natural language for HR person's specific needs or criteria for filtering. For example, user can say 'I want candidates with at least 5 years of experience in software development,' or 'Show me CVs with a master's degree in computer science.' you will diligently process the information and generate a tailored response ",
    model="gpt-3.5-turbo-1106",
    tools=[{"type": "retrieval"}]
)
def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )

    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
)
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

if st.button("Submit", type="primary"):
    if uploaded_file is not None and user_query:
        with st.spinner('Analyzing CVs...'):
            for uploaded_file in uploaded_file:
                temp_dir = "temp"
                temp_file_path = os.path.join(temp_dir, uploaded_file.name)  
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.write(f"Processed {uploaded_file.name}")
                file_response = client.files.create(
                    file=open(temp_file_path, "rb"),
                    purpose="assistants",
                )
                st.write(f"file_response {file_response}")
                print(f"file_response {file_response}")
            # temp_dir = "temp"
            # if not os.path.exists(temp_dir):
            #     os.makedirs(temp_dir)

            # temp_file_path = os.path.join(temp_dir, uploaded_file.name)            
            # with open(temp_file_path, "wb") as f:
            #     f.write(uploaded_file.getbuffer())
            try:
                # file_response = client.files.create(
                #     file=open(temp_file_path, "rb"),
                #     purpose="assistants",
                # )
                print("o")
                # assistant = client.beta.assistants.update(
                #     assistant_id= assistant.id,
                #     file_ids=[file_response.id],
                # )
                # thread = client.beta.threads.create()
                # run = submit_message(assistant.id, thread, user_query)
                # run = wait_on_run(run, thread)
                # response_messages = get_response(thread)
                # response = pretty_print(response_messages)
                # st.text_area("Response:", value=response, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")

