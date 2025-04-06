from fastapi import APIRouter
from fastapi import Depends
from services.movie_recommendation import Recommender
from services.setup import get_recommender
from models.api_models import MovieRequest

router = APIRouter()

@router.get("/")
def root():
    return {"hello":"world"}

@router.post("/recommend")
async def recommend(request:MovieRequest, recommendation_service:Recommender = Depends(get_recommender)):
    response = await recommendation_service.recommend(request.favorite_movie_with_reason, request.release_year_preference, request.mood_preference)
    return {"response":response}