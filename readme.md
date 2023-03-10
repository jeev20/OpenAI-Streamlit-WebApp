## OpenAI-Streamlit app deployed on a Raspberry Pi 4

### OpenAI API key as Enviornment variable
#### On Linux
To set the OpenAI API we can set an enviornment variable by navigating to `etc`. Here I use nano to open the `profile` contents. 
```bash
nano etc/profile
# at the end of the file add this 
export OPENAI_API_KEY="YOUR OPENAI API KEY"
```
To check all the environment variable is set we use 
```bash
printenv
```
#### On windows
Remember that newly set enviornment variables are only accessible after a restart of windows. 

``Start menu --> Edit system enviornment variables --> Enviornment variables --> System variable --> Add``

`OPENAI_API_KEY="YOUR OPENAI API KEY"`



### Bash script
Then we write a bash script with a tag `-l` which ensures enviornment variables are accessible. 

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