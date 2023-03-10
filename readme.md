## OpenAI-Streamlit app deployed on a Raspberry Pi 4
This integration uses the OpenAI API and explores their different models. In the first version of this streamlit app, 2 models ("gpt-3.5-turbo", "Dall-E2") are implemented along with a custom page showing search history by parsing a local log file. I do this by storing the promts and responses obtained to a log file. For `Dall-E2`, I save the images locally and then access them in the [3_📋_Search_History.py](https://github.com/jeev20/OpenAIIntegration/blob/master/pages/3_📋_Search_History.py) page. 

## Examples

![alt text](https://github.com/jeev20/OpenAIIntegration/blob/master/images/ChatGPTPage.JPG "ChatGPT Page")

![alt text](https://github.com/jeev20/OpenAIIntegration/blob/master/images/Dall-E2Page.JPG "Dall-E2 Page")

![alt text](https://github.com/jeev20/OpenAIIntegration/blob/master/images/SearchPageChatGPT.JPG "Search Page ChatGPT")


![alt text](https://github.com/jeev20/OpenAIIntegration/blob/master/images/SearchPageDall-E2.JPG "Search Page Dall-E2")

I host this app on a raspberrypi 4 which serves as my assistant. ChatGPT does improve troubleshooting and I do like having access to this superpower. 

Ideally, this implementation will be only on your network where the raspberrypi is connected. I use a OpenVPN solution to access this from anywhere in the world. This was developed during my vacation in India and deployed on a raspberrypi back home in Norway. Pretty fun!

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

## Authors

* *Initial commit* - [jeev20](https://github.com/jeev20)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jeev20/pigstack/blob/master/LICENSE) file for details

## Acknowledgments

* Thanks to folks at Streamlit and OpenAI 
