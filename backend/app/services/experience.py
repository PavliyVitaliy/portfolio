from odmantic import AIOEngine

from core.models import Experience, mongo_helper


async def get_experience(user_id: str) -> Experience:
    engine: AIOEngine = mongo_helper.get_engine()
    return await engine.find_one(Experience, Experience.user_id == user_id)
