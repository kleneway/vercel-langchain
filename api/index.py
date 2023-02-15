from os import environ
from flask import Flask, request
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.utilities import SerpAPIWrapper
from pickle import load as pickle_load
# from boto3 import client
from faiss import read_index

app = Flask(__name__)
# s3 = client("s3")

@app.route('/')
def home():
    # llm = OpenAI(temperature=0.1, max_tokens=2000, top_p=1, frequency_penalty=0, presence_penalty=0.6)
    # text = "What would be a good company name a company that makes colorful socks?"
    # print("text: ", text)
    return "Hello World!"

# @app.route('/upload/<username>/<file_type>', methods=['POST'])
# def upload(username, file_type):
#     try:
#         file = request.files["file"]
#     except KeyError:
#         return "No file uploaded"
    
#     if not username or not file_type:
#         return "Error: Invalid username or file type"

#     bucket_name = environ.get("BUCKET_NAME")
#     s3.upload_fileobj(file, bucket_name, f"{username}/{file_type}/{file.filename}", ExtraArgs={"ACL": "public-read"})

#     return  f"https://{bucket_name}.s3.amazonaws.com/{username}/{file_type}/{file.filename}"

@app.route('/ask/<username>', methods=['GET'])
def ask(username):
    try:
        question = request.args["question"]
    except KeyError:
        return "No question provided"

    # Load the LangChain.
    index = read_index(f"{username}_docs.index")

    # TODO: swap this out for a hosted vector store
    with open(f"{username}_faiss_store.pkl", "rb") as f:
        store = pickle_load(f)

    store.index = index
    chain = VectorDBQA.from_llm(llm=OpenAI(temperature=0), vectorstore=store)
    result = chain.run(question)
    return result

@app.route('/search', methods=['GET'])
def ask():
    try:
        query = request.args["q"]
    except KeyError:
        return "No query provided"

    search = SerpAPIWrapper()
    result = search.run(query)
    return result