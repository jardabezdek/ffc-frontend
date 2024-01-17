# :rocket: Frozen facts center frontend

The web application employing data visualization is constructed utilizing
[Streamlit](https://streamlit.io/).

## :construction_worker_man: Setup

### :wrench: Local development

In order to create a working environment, the [docker](https://www.docker.com/)
is used. To start it, please, follow the next steps.

1. Launch the docker daemon.
1. Get to the repository root folder.
1. Build the docker image with a proper tag: `docker build --tag ffc-fe:latest .`
1. Run docker container: `docker run -it -v $(pwd):/usr/src/app -p 8501:8501 ffc-fe:latest`
1. See the app running on the following link: [http://localhost:8501/](http://localhost:8501/)

### :envelope: Deployment

The following is written in [the official streamlit docs](https://docs.streamlit.io/streamlit-community-cloud/manage-your-app#manage-your-app-in-github):

> Your GitHub repository is the source for the app, so that means that any time you push an update
> to your repo you'll see it reflected in the app in almost real time. Try it out!
>
> Streamlit also smartly detects whether you touched your dependencies, in which case it will
> automatically do a full redeploy for you—which will take a little more time. But since most
> updates don't involve dependency changes, you should usually see your app update in real time.
