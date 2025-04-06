from openai import AsyncOpenAI

import os
from dotenv import load_dotenv
from supabase import create_async_client

load_dotenv()


class Recommender:
    """Service to recommend movies"""

    def __init__(self) -> None:
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.messages = [
            {
                "role": "system",
                "content": """You are an enthusiastic movie expert who loves recommending movies to people. 
                You will be given two pieces of information - some context about movies and a description about a type of movies a user likes. 
                Your main job is to formulate a short answer recommending a movie using the provided context.
                If you are unsure and cannot find the answer, say, "Sorry, I don't know the answer."
                Please do not make up the answer. Always speak as if you were chatting to a friend.""",
            }
        ]
        self.supabase_client = create_async_client(supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_API_KEY"))

    def _retrieve_documents(self):
        """an internal method that will do a semantic search on a vector database to find relevant documents"""
        pass

    def recommend(self):
        """recommend a movie based on the user interest and the relevant movies in the vector database"""
        pass