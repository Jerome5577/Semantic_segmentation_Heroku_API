# # p8 API_simple


#
FROM python:3.9.15


#
WORKDIR /app


RUN apt-get update
RUN apt-get install  -y


# 
COPY requirements.txt .
#
COPY . .


# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt



# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]
# 
CMD ["main.py"]


# RUN chmod +x start.sh
# CMD ["./start.sh"]
