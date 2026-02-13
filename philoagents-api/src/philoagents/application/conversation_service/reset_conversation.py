from loguru import logger
from pymongo import MongoClient
from philoagents.config import settings



async def reset_conversation_state():
    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGO_DB_NAME]
        
        collections_deleted = []
        if settings.MONGO_STATE_CHECKPOINT_COLLECTION in db.list_collection_names():
            db.drop_collection(settings.MONGO_STATE_CHECKPOINT_COLLECTION)
            collections_deleted.append(settings.MONGO_STATE_CHECKPOINT_COLLECTION)
            logger.info(f"Collection {settings.MONGO_STATE_CHECKPOINT_COLLECTION} deleted")
        if settings.MONGO_STATE_WRITES_COLLECTION in db.list_collection_names():
            db.drop_collection(settings.MONGO_STATE_WRITES_COLLECTION)
            collections_deleted.append(settings.MONGO_STATE_WRITES_COLLECTION)
            logger.info(f"Collection {settings.MONGO_STATE_WRITES_COLLECTION} deleted")

        client.close()

        if collections_deleted:
            return {"status": "success", "message": f"Collections deleted: {collections_deleted}"}
        else:
            return {"status": "success", "message": "No collections deleted"}
    except Exception as e:
        logger.error(f"Error resetting conversation: {e}")
        raise Exception(f"Error resetting conversation: {e}")