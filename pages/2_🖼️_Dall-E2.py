
# Show the promt to the user
import streamlit as st
import os
import openai
from datetime import datetime
import logging
for handler in logging.root.handlers[:]: # Removing handlers, this allows logging to a file
    logging.root.removeHandler(handler)
log_fmt = ("{\"time\": \"%(asctime)-s\", \"level\": \"%(levelname)-s\", \"logger\":\"Dall-E2\", \"message\": %(message)s}")
logging.basicConfig(
    level=logging.INFO,
    format=log_fmt,
    filename=os.path.join(os.path.dirname(os.path.realpath(__file__)),"logs", "execution.log"),
    filemode='a',
)

# Giving this log a name
logger = logging.getLogger("Dall-E2")

# Setting name of the page in Streamlit
st.set_page_config(
    page_title="Dall-E2",
    page_icon="🖼️",
)
    
def download_image(image_url, fullFilePath):
    """
    Helper function to save the image file to disk
    """
    import requests
    img_data = requests.get(image_url).content
    with open(fullFilePath, 'wb') as handler:
        handler.write(img_data)
    
# Show the promt to the user
ImagePromt = st.text_input(label="Promt",  placeholder="Provide your promt to create an image", label_visibility="hidden",)

if len(ImagePromt)>0:  # only send calls if promts are available
    #Authentication
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Image.create(
    prompt=ImagePromt,
    n=1,
    size="256x256"
    )
    image_url = response['data'][0]['url']
    
    st.markdown("***")
    # Show the output to the user
    st.markdown("![response]({0})".format(image_url))
    st.markdown("***")
    
    timestamp=datetime.now().strftime("%d_%m_%Y-%I_%M_%S_%p")
    fullFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"images","result_{0}.png".format(timestamp)).replace("\\","\\\\")
    download_image(image_url.strip(), fullFilePath)  # Download image to local disk
    # in logText replace " to ' to ensure our logs do not contain double quotes
    logText = "{\"Promt\":\"%s\",\"Response\":\"%s\", \"ImageLocation\":\"%s\"}" % (ImagePromt.replace('"','\''), image_url.strip(),fullFilePath)
    logger.info(logText)
    
else:
    st.markdown("***")
    st.markdown("#### Promts are required to generate images in Dall-E2")
    st.markdown("***")
