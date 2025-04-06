from services.movie_recommendation import Recommender
_recommender_instance: Recommender | None = None

async def get_recommender() -> Recommender:
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = await Recommender.setup_recommender()
    return _recommender_instance