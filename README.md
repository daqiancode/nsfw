# NSFW
nfsw AI model service with nsfw_image_detection and FastAPI
- DockerHub: https://hub.docker.com/r/daqiancode/nsfw
- Run: `docker run -d -p8000:8000 --name nswfw daqiancode/nsfw:0.0.1`
- API: http://localhost:8000/docs

### Installation
```
pip install -r requirements.txt

# dev mode
uvicorn app.main:app --reload
```