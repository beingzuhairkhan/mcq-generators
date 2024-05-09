import pandas as pd
import os
import json
import traceback
from dotenv import load_dotenv
from src.mcqGen.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqGen.logger import logging
from src.mcqGen.McqGen import generate_evaluate_chain

# Load environment variables
load_dotenv()

# Load response JSON
response_path = 'C:\\Users\\zuhai\\OneDrive\\Desktop\\PROJECT2\\MCQ_GENERATOR\\Response.json'
if os.path.exists(response_path):
    with open(response_path, 'r') as file:
        RESPONSE_JSON = json.load(file)
else:
    st.error("Response JSON file not found. Please ensure that the file path is correct.")

# Streamlit application title
st.title("MCQ creator application with LangChain")

# Define a default value for response
response = None

# Form for user inputs
with st.form("user_inputs"):
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")
    # Input fields
    mcq_count = st.number_input("No of MCQ", min_value=3, max_value=50)
    subject = st.text_input("Insert subject", max_chars=20)
    tone = st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")
    # Create MCQs button
    button = st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                # Generate MCQs
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
            except FileNotFoundError:
                st.error("File not found. Please ensure that you have uploaded a valid file.")
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"An error occurred: {str(e)}")
            else:
                if isinstance(response, dict):
                    # Extract the quiz data
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            # Display the generated MCQs in a table
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the review
                            st.text_area(label="Review", value=response.get("review", ""))
                    else:
                        st.error("Error in the table data")
    else:
        st.write(response)
