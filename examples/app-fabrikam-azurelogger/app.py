# app.py
import os
from fastapi import FastAPI
from loggermanager import get_logger_provider
from dotenv import load_dotenv

load_dotenv()

logger = get_logger_provider("azure_appinsights")

app = FastAPI()


@app.get("/")
async def read_root():
    logger.log_info("Received request at root endpoint.")
    return {"message": "up & running"}


@app.get("/products/{product_id}")
async def read_item(product_id: int):
    logger.log_info(f"Received request for item {product_id}.")
    try:
        if product_id == 0:
            raise ValueError("Invalid item ID.")
        return {"item_id": product_id, "value": f"Item {product_id}"}
    except Exception as e:
        logger.log_error(f"Error retrieving item {product_id}: {e}")
        return {"error": str(e)}
