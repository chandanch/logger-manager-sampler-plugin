# app.py
import os
from fastapi import FastAPI
from loggermanager import get_logger_provider
from dotenv import load_dotenv

load_dotenv()

logger = get_logger_provider(
    "aws_cloudwatch",
    log_group=os.getenv("AWS_LOG_GROUP_NAME"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

app = FastAPI()


@app.get("/")
async def read_root():
    logger.log_info("Received request at root endpoint.")
    return {"status": "up & running"}


@app.get("/castles/{item_id}")
async def read_item(item_id: int):
    logger.log_info(f"Received request for item {item_id}.")
    try:
        # Simulate data retrieval
        if item_id == 0:
            raise ValueError("Invalid item ID.")
        return {"item_id": item_id, "value": f"Item {item_id}"}
    except Exception as e:
        logger.log_error(f"Error retrieving item {item_id}: {e}")
        return {"error": str(e)}
