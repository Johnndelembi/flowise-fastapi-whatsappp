import os
import logging
from fastapi import FastAPI, Request, Query
from fastapi.responses import Response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler("app.log"),  # File output
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Get environment variables
MY_TOKEN = os.getenv("MYTOKEN", "12345")
PORT = os.getenv("PORT", 8001)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Webhook is listening at {PORT}")

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    """Verify webhook subscription with Meta."""
    logger.info("logs to remove")
    if hub_mode and hub_verify_token:
        if hub_mode == "subscribe" and hub_verify_token == MY_TOKEN:
            logger.info("Webhook verified successfully")
            return Response(content=hub_challenge, media_type="text/plain")
        else:
            logger.warning("Webhook verification failed")
            return Response(status_code=403)
    logger.warning("Missing mode or token in webhook verification request")
    return Response(status_code=400)

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming WhatsApp messages."""
    logger.info("Webhook calls>>>>")
    try:
        body_param = await request.json()
        logger.info("Message Received")
        logger.info(f"request body: {body_param}")

        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return Response(status_code=200)

@app.get("/")
async def root():
    return "Hello Ansh this is webhook setup" 