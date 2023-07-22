# arcgis-documentation-helper
backend

# Usage 
1. add .env 
e.g. 
```
REDIS_URL=redis://
OPENAI_API_KEY=sk-
```
2. install and run ingest
```
pip install -r requirements.txt

cd ingest
python ingest.py

```

3. host the server

```

bash run.sh
# or
uvicorn api.app:app --host 0.0.0.0 --port 3000
```