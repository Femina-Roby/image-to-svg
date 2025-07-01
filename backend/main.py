import os
from dotenv import load_dotenv
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from ariadne import QueryType, MutationType, make_executable_schema, upload_scalar
from ariadne.asgi import GraphQL

from model import convert_image_to_svg  # your existing local converter

# 1) Load HF API key
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise RuntimeError("HF_API_KEY not set in environment")

# 2) StarVector inference function
def call_starvector(image_bytes: bytes) -> str:
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    files = {"image": ("upload", image_bytes, "application/octet-stream")}
    resp = requests.post(
        "https://api-inference.huggingface.co/models/StarVector/StarVector",
        headers=headers,
        files=files,
        timeout=120,
    )
    resp.raise_for_status()
    return resp.text  # should be SVG markup

# 3) Define GraphQL schema
type_defs = """
  scalar Upload

  type Query {
    hello(name: String!): String!
  }

  type Mutation {
    uploadImage(file: Upload!): String!
  }
"""

query = QueryType()
mutation = MutationType()

@query.field("hello")
def resolve_hello(_, info, name):
    return f"Hello, {name}!"

@mutation.field("uploadImage")
async def resolve_upload_image(_, info, file):
    # read the raw bytes
    image_bytes = await file.read()
    print("Received file size:", len(image_bytes))

    # try HF StarVector first
    try:
        svg = await run_in_threadpool(call_starvector, image_bytes)
    except Exception as hf_err:
        print("StarVector inference failed:", hf_err)
        # fallback to local converter
        svg = await run_in_threadpool(convert_image_to_svg, image_bytes)

    return svg

schema = make_executable_schema(type_defs, [query, mutation, upload_scalar])
graphql_app = GraphQL(schema, debug=True)

# 4) Mount FastAPI + CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/graphql", graphql_app)

# optional health-check
@app.get("/")
def health_check():
    return {"status": "ok"}