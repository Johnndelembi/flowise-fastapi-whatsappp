# 3rd Party WhatsApp (FastAPI, Flowise) Integration

This project provides a FastAPI-based webhook for integrating WhatsApp messaging with an external AI or automation API. When a user sends a message to your WhatsApp number, the webhook receives the message, forwards it to an external API for processing, and sends the API's response back to the user on WhatsApp.

---

## Features

- **Webhook Verification**: Handles WhatsApp webhook verification with Meta.
- **Message Handling**: Receives WhatsApp messages, extracts the sender and message text.
- **External API Integration**: Forwards incoming messages to an external API (e.g., AI chatbot) and retrieves the response.
- **Automated Replies**: Sends the API's response back to the original sender on WhatsApp.
- **Logging**: Logs all incoming requests and outgoing responses for debugging and monitoring.

---

## Folder Structure

```
whatsapp-test/
├── webhook.py
├── webhook_2.py
├── app.log
├── .env
└── README.md
```

---

## Requirements

- Python 3.8+
- WhatsApp Business API or WhatsApp Cloud API credentials
- External API endpoint for processing messages (e.g., AI chatbot)
- [ngrok](https://ngrok.com/) or similar tool for local development (optional)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/whatsapp-webhook-fastapi.git
cd whatsapp-webhook-fastapi/whatsapp-test
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv requests
```

### 3. Configure Environment Variables

Create a `.env` file in the project directory with the following content:

```
MYTOKEN=your_webhook_verify_token
WHATSAPP_TOKEN=your_whatsapp_api_token
PHONE_NUMBER_ID=your_whatsapp_phone_number_id
PORT=8000
```

- `MYTOKEN`: Token for webhook verification with Meta.
- `WHATSAPP_TOKEN`: Your WhatsApp API access token.
- `PHONE_NUMBER_ID`: Your WhatsApp phone number ID.
- `PORT`: Port to run the FastAPI server (default: 8000).

### 4. Update API URLs

In `webhook_2.py`, update these variables:

```python
API_URL = "http://127.0.0.1:3000/api/v1/prediction/your-model-id"  # Your external API endpoint
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
```

Replace `{PHONE_NUMBER_ID}` with your actual phone number ID or use the environment variable.

---

## Running the Server

```bash
uvicorn webhook_2:app --reload --port 8000
```

---

## Exposing the Webhook (for Meta/WhatsApp)

If running locally, use [ngrok](https://ngrok.com/) to expose your server:

```bash
ngrok http 8000
```

Copy the HTTPS URL provided by ngrok and use it as your webhook URL in the WhatsApp Business API dashboard.

---

## Endpoints

### `GET /webhook`

- Used by Meta to verify your webhook.
- Requires query parameters: `hub.mode`, `hub.challenge`, `hub.verify_token`.

### `POST /webhook`

- Receives WhatsApp messages.
- Extracts the sender's number and message text.
- Forwards the message to your external API.
- Sends the API's `"text"` response back to the sender on WhatsApp.

### `GET /`

- Health check endpoint. Returns a welcome message.

---

## Example Workflow

1. User sends "Hello" to your WhatsApp number.
2. WhatsApp forwards the message to your webhook (`POST /webhook`).
3. The webhook extracts the message and sender, sends the message to your external API.
4. The external API responds with a JSON like:
    ```json
    {
      "text": "Bonjour! 🌟 Welcome to your cozy Parisian getaway! ...",
      "question": "Hello",
      ...
    }
    ```
5. The webhook sends only the `"text"` value back to the user on WhatsApp.

---

## Logging

All requests and responses are logged to `app.log` and the console for debugging.

---

## Troubleshooting

- **Webhook Not Verified**: Ensure `MYTOKEN` matches the token set in the Meta dashboard.
- **No Response Sent**: Check logs for extraction errors or API failures.
- **WhatsApp API Errors**: Ensure your `WHATSAPP_TOKEN` and `PHONE_NUMBER_ID` are correct and have permission to send messages.

---

## License

MIT License

---

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [ngrok](https://ngrok.com/)

---

## Contact

For questions or support, open an issue or contact [your-email@example.com](mailto:your-email@example.com).