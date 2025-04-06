from pydantic import BaseModel

class MovieRequest(BaseModel):
    favorite_movie_with_reason:str
    release_year_preference: str
    mood_preference: str