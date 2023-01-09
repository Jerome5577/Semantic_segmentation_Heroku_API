

#
#uvicorn main:app --host 0.0.0.0 --port ${PORT} --reload


web: gunicorn --reload  --workers 2 --host 0.0.0.0 --port ${PORT} main:app 