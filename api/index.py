
import os
import logging
from flask import Flask, request
from langchain.llms import OpenAI
import boto3


app = Flask(__name__)
s3 = boto3.client("s3")


@app.route('/')
def home():
    llm = OpenAI(temperature=0.1, max_tokens=2000, top_p=1, frequency_penalty=0, presence_penalty=0.6)
    text = "What would be a good company name a company that makes colorful socks?"
    print("text: ", text)
    return "Hello World!"
    # return llm(text)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files["file"]
    except KeyError:
        return "No file uploaded"
    
    print("Got file: ", file.filename)
    bucket_name = os.environ.get("BUCKET_NAME")

    print("Uploading to bucket: ", bucket_name)
    s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={"ACL": "public-read"})

    print("Uploaded successfully")
    print("url: ", f"https://{bucket_name}.s3.amazonaws.com/{file.filename}")

    return 'File successfully uploaded'
