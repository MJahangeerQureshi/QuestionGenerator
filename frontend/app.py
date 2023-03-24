import os
import json
import requests
import pandas as pd
import streamlit as st

st.title("Auto-Suggest QGen (with ML & GPT3)")

input_text = st.text_area("Enter Text")

if st.button("Auto Suggest Questions"):
    with st.spinner("Reading and Thinking of Questions"):
        response = requests.request("POST", 
                                    url="http://localhost:9004/suggest_questions/",
                                    headers={
                                            'Content-Type': 'application/json'
                                            }, 
                                    data=json.dumps({
                                                    "input_text": input_text
                                                    }))

        questions = pd.DataFrame(response.json())
        
        with st.expander("Suggested Questions and their Context"):
            st.table(questions)


