
import os
from flask import Flask, request
from langchain.llms import OpenAI
import boto3

app = Flask(__name__)
s3 = boto3.client("s3")

@app.route('/')
def home():
    llm = OpenAI(temperature=0.9)
    text = "What would be a good company name a company that makes colorful socks?"
    return "Hello World!"
    # return llm(text)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files["file"]
    bucket_name = os.environ.get("BUCKET_NAME")
    s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={"ACL": "public-read"})
    return 'File successfully uploaded'
