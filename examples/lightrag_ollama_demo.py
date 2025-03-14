import asyncio
import os
import inspect
import textract
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc

WORKING_DIR = "book_ollama/working_dir_csv/"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)
#change in the model name
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    #llm_model_name="gemma2",
    #llm_model_name="mistral-nemo",
    #llm_model_name="dolphin-mistral",
    llm_model_name="qwen2.5",
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}},
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embedding(
            texts, embed_model="nomic-embed-text", host="http://localhost:11434"
        ),
    ),
)

# with open("./book.txt", "r", encoding="utf-8") as f:
#     rag.insert(f.read())

file_path = 'book_ollama/output.csv'
text_content = textract.process(file_path)

rag.insert(text_content.decode('utf-8'))

# Perform naive search
print(
    rag.query("What do you understand from this document on the perspective of OBE?", param=QueryParam(mode="naive"))
)

# Perform local search
print(
    rag.query("Show the mappings of which CO maps to PO", param=QueryParam(mode="local"))
)

# Perform global search
print(
    rag.query("What is the course code of the document? Show the mappings of which CO maps to PO.", param=QueryParam(mode="global"))
)

# Perform hybrid search
print(
    rag.query("What is this document about?", param=QueryParam(mode="hybrid"))
)

# stream response
# resp = rag.query(
#     "What are the top themes in this story?",
#     param=QueryParam(mode="hybrid", stream=True),
# )


# async def print_stream(stream):
#     async for chunk in stream:
#         print(chunk, end="", flush=True)


# if inspect.isasyncgen(resp):
#     asyncio.run(print_stream(resp))
# else:
#     print(resp)
