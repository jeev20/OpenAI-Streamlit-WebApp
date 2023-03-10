import streamlit as st
import os
import openai
import json
import ast
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
log_fmt = ("{\"time\": \"%(asctime)-s\", \"level\": \"%(levelname)-s\", \"logger\":\"ChatGPT\", \"message\": %(message)s}")
logging.basicConfig(
    level=logging.INFO,
    format=log_fmt,
    filename=os.path.join(os.path.dirname(os.path.realpath(__file__)),"logs", "execution.log"),
    filemode='a',
)

logger = logging.getLogger("ChatGPT")


st.set_page_config(
    page_title="ChatGPT",
    page_icon="💬",
)

# Show promt to the user
promt = st.text_input(label="Promt", placeholder="Provide your promt",label_visibility="hidden",)


if len(promt)>0:  # only send calls if promts are available
    #Authentication
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": promt}
    ]
    )

    st.markdown("***")
    # Show the output to the user
    st.markdown("#### Response from ChatGPT")
    st.markdown(completion.choices[0].message.content)
    strippedResponse = completion.choices[0].message.content.strip(os.linesep).replace('\n', 'NEWLINE') # removes line separator and mentions where newlines are. When we parse we can reverse this to get a good markdown visualization
    # removes " to ' to ensure our logs do not contain double quotes
    strippedResponse = strippedResponse.replace('"','\'')  
    promt = promt.replace('"','\'') 
    logText = "{\"Promt\":\"%s\",\"Response\":\"%s\"}" % (promt, strippedResponse)  
    logger.info(logText)
    #logger.info("|Promt:%s",promt+"|Response:"+ strippedResponse+"|")
    st.markdown("***")
else:
    st.markdown("***")
    st.markdown("#### Promts are required to generate responses in ChatGPT")
    st.markdown("***")
