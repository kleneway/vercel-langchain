import os
from flask import Flask, request
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
import pickle
import boto3
import faiss

app = Flask(__name__)
s3 = boto3.client("s3")

@app.route('/')
def home():
    # llm = OpenAI(temperature=0.1, max_tokens=2000, top_p=1, frequency_penalty=0, presence_penalty=0.6)
    # text = "What would be a good company name a company that makes colorful socks?"
    # print("text: ", text)
    return "Hello World!"

@app.route('/upload/<username>/<file_type>', methods=['POST'])
def upload(username, file_type):
    try:
        file = request.files["file"]
    except KeyError:
        return "No file uploaded"
    
    if not username or not file_type:
        return "Error: Invalid username or file type"

    bucket_name = os.environ.get("BUCKET_NAME")
    s3.upload_fileobj(file, bucket_name, f"{username}/{file_type}/{file.filename}", ExtraArgs={"ACL": "public-read"})

    return  f"https://{bucket_name}.s3.amazonaws.com/{username}/{file_type}/{file.filename}"

@app.route('/ask/<username>', methods=['GET'])
def ask(username):
    try:
        question = request.args["question"]
    except KeyError:
        return "No question provided"

    # Load the LangChain.
    index = faiss.read_index(f"{username}_docs.index")

    # TODO: swap this out for a hosted vector store
    with open(f"{username}_faiss_store.pkl", "rb") as f:
        store = pickle.load(f)

    store.index = index
    chain = VectorDBQA.from_llm(llm=OpenAI(temperature=0), vectorstore=store)
    result = chain.run(question)
    return result