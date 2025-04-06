from langchain_text_splitters import CharacterTextSplitter
from openai import OpenAI
import os
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase_client = create_client(supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_API_KEY"))
def split_documents(path:str)->list:
    """split documents into chuncks"""
    with open(path, "r") as movies_file:
        content = movies_file.read()
    # define the text splitter

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size = 250,
        chunk_overlap= 35,
        length_function=len,
        is_separator_regex=False,
        
    )
    texts = text_splitter.create_documents([content])
    # print(texts)
    return texts

def embed_document(chunks:list)->dict:
    """embed documents or chunks"""
    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk.page_content ,
            model="text-embedding-ada-002"
        )
       
        data = {
            "content":chunk.page_content ,
            "embedding":response.data[0].embedding
        }
        supabase_client.table("movie_documents").insert(data).execute()
    return "embedding sucessfully stored on supabase"


if __name__ =="__main__":
    chunks = split_documents("./data/movies.txt")
    result = embed_document(chunks)
    print(result)