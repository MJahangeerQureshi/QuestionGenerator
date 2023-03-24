import os
import json
import requests
import pandas as pd
import streamlit as st

# Streamlit app to auto-suggest questions using ML & GPT3
st.title("Auto-Suggest QGen (with ML & GPT3)")

# Input text from user
input_text = st.text_area("Enter Text")

# When button pressed, auto-suggest questions
if st.button("Auto Suggest Questions"):
    with st.spinner("Reading and Thinking of Questions"):
        # Make POST request to localhost
        response = requests.request("POST", 
                                    url="http://localhost:9004/suggest_questions/",
                                    headers={
                                            'Content-Type': 'application/json'
                                            }, 
                                    data=json.dumps({
                                                    "input_text": input_text
                                                    }))
        # Convert response to dataframe
        questions = pd.DataFrame(response.json())
        
        # Display suggested questions and context
        with st.expander("Suggested Questions and their Context"):
            st.table(questions)