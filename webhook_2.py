import os
import logging
from fastapi import FastAPI, Request, Query
from fastapi.responses import Response, JSONResponse
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_URL = "your-flowsier-api-url"  # Replace with your Flowsier API URL
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "1234")  # Replace with your phone number ID
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/{replace_with_phone_number_id}/messages"  # Replace with your phone number ID
WHATSAPP_TOKEN = "your-whatsapp-token"  # Replace with your WhatsApp token

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

def send_whatsapp_message(recipient_number: str, message: str):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    logging.info(f"WhatsApp API response: {response.status_code} {response.text}")
    return response.status_code == 200

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
MY_TOKEN = os.getenv("MYTOKEN", "Ansh_token")
PORT = os.getenv("PORT", 8000)

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

        # Extract the message text and sender's number from the WhatsApp webhook payload
        message_text = None
        sender_number = None
        try:
            message_text = body_param["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            sender_number = body_param["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        except Exception as e:
            logger.warning(f"Could not extract message text or sender: {e}")

        if message_text and sender_number:
            api_response = query({"question": message_text})
            logger.info(f"API response: {api_response}")

            # Prepare the message to send back (only the "text" field)
            if isinstance(api_response, dict) and "text" in api_response:
                reply_text = api_response["text"]
            else:
                reply_text = str(api_response)

            send_whatsapp_message(sender_number, reply_text)
            return JSONResponse(content={"status": "sent"}, status_code=200)
        else:
            logger.warning("No message text or sender found in webhook payload")
            return Response(status_code=204)

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return Response(status_code=200)

@app.get("/")
async def root():
    return "Hello Ansh this is webhook setup" 