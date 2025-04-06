import asyncio
from openai import AsyncOpenAI

import os
from dotenv import load_dotenv
from supabase import create_async_client

load_dotenv()


class Recommender:
    """Service to recommend movies"""

    def __init__(self, openai_client, supabase_client) -> None:
        self.openai_client = openai_client
        self.supabase_client = supabase_client
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
    
    @classmethod
    async def setup_recommender(cls):
        openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        supabase_client = await create_async_client(
            supabase_url=os.getenv("SUPABASE_URL"),
            supabase_key=os.getenv("SUPABASE_API_KEY")
        )
        return cls(openai_client, supabase_client)
    async def _retrieve_documents(self, favorite_movie_with_reason:str, release_year_preference:str, mood_preference:str)->list:
        """an internal method that will do a semantic search on a vector database to find relevant documents"""
        query = f"favorite movie:{favorite_movie_with_reason} release year preference:{release_year_preference} mood preference:{mood_preference}"
        embedding_response = await self.openai_client.embeddings.create(
        model="text-embedding-ada-002",  # or text-embedding-ada-002
        input=query
        )

        embedding_vector = embedding_response.data[0].embedding
        response = await self.supabase_client.rpc(
            "match_movies",
            {
                "query_embedding":embedding_vector,
                "match_threshold":0.5,
                "match_count":1
            }
        ).execute()

        document = response.data[0]["content"]
    def recommend(self):
        """recommend a movie based on the user interest and the relevant movies in the vector database"""
        pass




if __name__ == "__main__":
    async def main():
        recommender = await Recommender.setup_recommender()
        await recommender._retrieve_documents(
            "The Shawshank Redemption Because it taught me to never give up hope no matter how hard life gets",
            "I want to watch movies that were released after 1990",
            "I want to watch something stupid and fun"
        )

    asyncio.run(main())