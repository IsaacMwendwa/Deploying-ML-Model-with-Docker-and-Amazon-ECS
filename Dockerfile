FROM python:3.11.5
# 
WORKDIR /Deployment
# 
COPY . .
# 
RUN pip install --no-cache-dir --upgrade -r /Deployment/requirements.txt 
#
CMD ["flask", "run", "--host", "0.0.0.0"]
