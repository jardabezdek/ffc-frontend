## :rocket: Frozen facts center frontend

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
