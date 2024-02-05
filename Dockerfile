FROM python:3.6.9
# 
WORKDIR /Deployment
# 
COPY . .
# 
RUN pip install --no-cache-dir --upgrade -r /Deployment/requirements.txt 
#
CMD ["flask", "run", "--host", "0.0.0.0"]