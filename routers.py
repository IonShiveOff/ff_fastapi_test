import logging

import httpx
from fastapi import HTTPException, APIRouter

from models import InputData
from redis_utils import get_request_response, store_request_response
from utils import DataProcessing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/process_data/")
async def process_data(input_data: InputData):
    """
    Processes incoming client data,
    fetches an external API response,
    stores into or retrieves data from Redis,
    returns result JSON.

    Args:
        input_data (InputData): Incoming JSON. Expected to contain client_id and iin_bin

    Returns:
        dict: A dictionary object containing the processed raw data and a random fact about cats.
    """
    try:
        logger.info(f"Received data: {input_data}")
        request_id = str(input_data.client_id)
        iin_bin = input_data.iin_bin

        redis_data = await get_request_response(request_id)
        logger.info(f"Got data from Redis: {redis_data}")
        if redis_data:
            return {"input_data": input_data,
                    "valid_iin_bin": redis_data.get('valid_iin_bin'),
                    "cat_fact": redis_data.get('cat_fact')}

        _dp = DataProcessing()
        valid_iin_bin = _dp.validate_identification_number(iin_bin)
        logger.info(f"IIN/BIN is valid: {valid_iin_bin}")

        async with httpx.AsyncClient() as client:
            response = await client.get("https://catfact.ninja/fact")
            logger.info("Send get request to an external API")
            response.raise_for_status()
            cat_fact = response.json()
            logger.info("Got random cat fact")

        store_data = {'valid_bin_iin': valid_iin_bin, 'cat_fact': cat_fact}
        await store_request_response(request_id, data=store_data)
        logger.info(f"Stored data for iin_bin {request_id}: {store_data}")

        return {"input_data": input_data,
                "valid_iin_bin": valid_iin_bin,
                "cat_fact": cat_fact}

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
