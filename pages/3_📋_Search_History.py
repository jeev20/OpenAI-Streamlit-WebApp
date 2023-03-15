import streamlit as st
import os
import json
from itertools import cycle
from PIL import Image

st.markdown("#### Parse search history")

# Give user the model options to choose from
models = ["ChatGPT", "Dall-E2"]  
selected_model = st.radio("Choice", options=models, label_visibility="hidden",)
st.markdown("******")

# Assign the log file path
log_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"logs", "execution.log")

log_items = []

# Only read the file once
with open(log_filepath) as f:
    f = f.readlines()

# Save the lines to memory in log_items
for line in f:
    log_items.append(line)
    
# Populate promts and responses for given models 
responses = [] # your images here
promts = [] # your caption here
for log in log_items:  # iterate through the list (for line in logs)
    # Here we fetch and filter logs to the selected model. 
    import json 
    data = json.loads(log)
    if selected_model=="ChatGPT" and data["logger"]=="ChatGPT":
        responses.append(data["message"]["Response"])
        promts.append(data["message"]["Promt"])
    elif selected_model=="Dall-E2" and data["logger"]=="Dall-E2":
        responses.append(data["message"]["ImageLocation"])
        promts.append(data["message"]["Promt"])
    
        
# Given the type of the model show the results in a custom way
# Each model can be treated seperately depending on how we saved the promt and responses the log file
if selected_model=="ChatGPT":  # Logic for ChatGPT
    cols = cycle(st.columns(1))    
    for idx, response in enumerate(responses):
        next(cols).markdown("**Promt**: %s" % promts[idx].replace('\'','"') )  # Ensures that quotes given in the promt are parsed correctly from the logs
        next(cols).markdown("**Response**: %s" %(response.replace('\'','"').replace('NEWLINE','\n',)))  # Ensures that we get a nice markdown same as the original response from OpenAI
        next(cols).markdown("******")
elif selected_model=="Dall-E2":  # Logic for Dall-E2
    cols = cycle(st.columns(2))    
    for idx, response in enumerate(responses):
        image = Image.open(response)
        next(cols).image(image, width=256, caption=promts[idx].replace('\'','"'))         
            
    
        
  
