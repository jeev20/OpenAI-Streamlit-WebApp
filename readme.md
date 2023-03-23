## OpenAI-Streamlit app deployed on a Raspberry Pi 4
This streamlit multi-page webapp explores the different models from OpenAI API. In the first version of this streamlit app, 2 models ("gpt-3.5-turbo", "Dall-E2") are implemented along with a custom page showing the search history (server side) by parsing a local log file. I do this by storing the promts and responses obtained to a log file. For `Dall-E2`, I save the images locally from the response web url and then access them in the [3_📋_Search_History](https://github.com/jeev20/OpenAI-Streamlit-WebApp/blob/master/pages/3_📋_Search_History.py) page. 

The cool thing about the `Search History` page is that it preserves the markdown syntax similar to the original response. The code blocks remain as code blocks and makes it visually easier to read the historical promts and responses. The `Search History` pages allows me to quickly look through the past promts and avoid redundant promts (saving on API token usage). 

 --------------------------------------------------

<details>
 <summary>Table of contents</summary>
 
- [OpenAI-Streamlit app deployed on a Raspberry Pi 4](#openai-streamlit-app-deployed-on-a-raspberry-pi-4)
- [Usage](#usage)
  - [Using docker compose](#using-docker-compose)
  - [Using docker run](#using-docker-run)
    - [Caveat with docker](#caveat-with-docker)
  - [Usage local execution](#usage-local-execution)
  - [OpenAI API key as Environment variable](#openai-api-key-as-environment-variable)
- [Screenshots](#screenshots)
    - [ChatGPT (generation and history retreival)](#chatgpt-generation-and-history-retreival)
    - [Dall-E2 (generation and history retreival)](#dall-e2-generation-and-history-retreival)
- [Hosting with OpenVPN](#hosting-with-openvpn)
  - [Bash script](#bash-script)
  - [Start on reboot](#start-on-reboot)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)



</details>

 --------------------------------------------------

## Usage 
### Using docker compose
* Clone this repository
* `cd` into the cloned repository
* Create a `.env` file with the following content
  ```bash 
  OPENAI_API_KEY=YOUR API KEY
  ```
* Run `docker compose up` will build and start the container 
* Open the browser with address `http://localhost:8501` or `http://YOURLOCALIP:8501`
* To close the container `docker compose down`
  
<details>
<summary> Using docker run</summary>

### Using docker run
* Clone this repository
* `cd` into the cloned repository
* Build the image note the `.` signifying the current directory
  ```bash 
  docker build -t openai-streamlit-webapp .
  ```
* Run the container (`--name` names the container, `-e` passes an environment variable into the container)
  In windows
  ```bash 
  docker run -p 8501:8501 --name openai-streamlit-webapp -e OPENAI_API_KEY=$env:OPENAI_API_KEY  openai-streamlit-webapp
  ```
  In linux
  ```bash 
  docker run -p 8501:8501 --name openai-streamlit-webapp -e OPENAI_API_KEY=$OPENAI_API_KEY  openai-streamlit-webapp
  ```
* Open the browser with address `http://localhost:8501` or `http://YOURLOCALIP:8501`
* For subsequent runs `docker start openai-streamlit-webapp`
  
</details>

#### Caveat with docker
The negative with running this on docker is that you will have to setup additional volumes on the host machine which are mapped to the containers folders `images` and `logs`. Doing this will ensure that you have all historical promts saved on disk and the images or logs are not wiped out when deleting the container. 

### Usage local execution
* Clone this repository 
* Set an enviornmental variable for the [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) (see below how this is done in linux and windows)
* `cd` into the cloned repository
* Create a virtual environment in the repository (i use virtualenv : `virtualenv env`)
* Activate your virtual environment `source env/bin/activate` on linux OR `.\env\Scripts\activate.ps1` on windows
* Run `pip install -r requirements.txt` within your virtual environment
* Run `streamlit run .\OpenAI_Demos.py` a browser will be opened at `http://localhost:8501` or `http://YOURLOCALIP:8501`

### OpenAI API key as Environment variable
1. On Linux
  
    To set the OpenAI API we can set an enviornment variable by navigating to `etc`. Here I use nano to open the `profile` contents. 
    ```bash
    nano etc/profile
    # at the end of the file add this 
    export OPENAI_API_KEY="YOUR OPENAI API KEY"
    ```
    To check all the environment variables we can use 
    ```bash
    printenv
    ```
    To check a specific one we can use `echo`  
    ```bash
    echo $OPENAI_API_KEY
    ```
2. On windows
   
    **Remember that newly set enviornment variables are only accessible after a restart of windows.** 

    ``Start menu --> Edit system enviornment variables --> Enviornment variables --> System variable --> Add``

    `OPENAI_API_KEY="YOUR OPENAI API KEY"`

    To check if the environment variable is set after the restart, open `PowerShell.exe` and use the following command to check if the API key is set correctly.   
    ```powershell
    echo $env:OPENAI_API_KEY
    ```

## Screenshots

#### ChatGPT (generation and history retreival)

![alt text](https://github.com/jeev20/OpenAI-Streamlit-WebApp/blob/master/images/ChatGPTPage.JPG "ChatGPT Page")

![alt text](https://github.com/jeev20/OpenAI-Streamlit-WebApp/blob/master/images/SearchPageChatGPT.JPG "Search Page ChatGPT")

#### Dall-E2 (generation and history retreival)

![alt text](https://github.com/jeev20/OpenAI-Streamlit-WebApp/blob/master/images/Dall-E2Page.JPG "Dall-E2 Page")

![alt text](https://github.com/jeev20/OpenAI-Streamlit-WebApp/blob/master/images/SearchPageDall-E2.JPG "Search Page Dall-E2")


## Hosting with OpenVPN

I host this app on a raspberrypi 4 which I run 24x7. It is hardwired to my Asus router. I use local execution approach, but in hindsight using docker with mapped drives to my NAS could have been a more elegant solution. I could have also used the docker dameon to run the container on reboot and avoided the crontab task. You can modify the docker-compose.yml to get this working as you wish. 

By default this implementation will only be accessible on your network where the raspberrypi / server is connected. But that is not good enough. 

To make it accessible anywhere in the world, I use a OpenVPN server (from my Asus Router). The first version was developed during my vacation in India and deployed on a raspberrypi back home in Norway. It is pretty cool to have access to your home network anywhere you go!

<details>
 <summary>Restart on reboot </summary>
### Bash script
Then we write a bash script with a tag `-l` which ensures enviornment variables are accessible when the script is run from crontab. 

The `source` and `streamlit run` both need the full path to their respective files. We finally save this file as `RunChatGPT.sh`
```bash
#!/bin/bash -l
# Let's call this script RunChatGPT.sh
source "home/raspi4/Dokumenter/ChatGPTIntegration/env/bin/activate"
streamlit run "home/raspi4/Dokumenter/ChatGPTIntegration/OpenAI_Demos.py"
```

### Start on reboot
Ideally, we want our streamlit app to restart automatically after the raspberrypi reboots. We can do this by updating the crontab. To open crontab on nano use the following. 

```bash
sudo crontab -e
```
Add the following at the end of `crontab` file
``` bash
@reboot /home/raspi4/RunChatGPT.sh
```
This should then run streamlit when the raspberrypi reboots. 


</details>

-----------------------------------------------------------

## Authors

* *Initial commit* - [jeev20](https://github.com/jeev20)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jeev20/OpenAI-Streamlit-WebApp/blob/master/LICENSE) file for details

## Acknowledgments


Thanks to folks at [Streamlit](https://github.com/streamlit/streamlit) and [OpenAI](https://openai.com).

ChatGPT does improve troubleshooting and helps me be a better developer and I do like having access to this superpower. Thank you Streamlit for making it so easy to run such demos. 
