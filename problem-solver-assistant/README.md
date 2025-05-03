

## Create virutal envirpnment

```
python3 -m venv venv

source venv/bin/activate && pip install -r requirements.txt
```


## Run API Server

```
uvicorn agent_api:app --reload --port 8000

```