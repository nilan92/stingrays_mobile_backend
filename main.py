from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
from datetime import datetime

app = FastAPI(title="Stingrays Webhook Receiver")

@app.get("/")
async def health():
    return {"status": "ok", "service": "webhook-receiver"}

@app.post("/webhooks/sms")
async def receive_sms_webhook(request: Request):
    # 1) Read the raw data they sent
    raw_body = await request.body()

    # 2) Graceful Error Handling: Try to parse the JSON
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except Exception:
        # If they send weird/broken data, log it so you can see what went wrong
        print("\n--- ERROR: INVALID JSON RECEIVED ---")
        print("Raw body:", raw_body)
        print("------------------------------------\n")
        # Return a clean 400 error so they know their formatting was off,
        # but your server stays online and healthy.
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    # 3) Accept EVERYTHING and log it to your console
    print("\n--- WEBHOOK RECEIVED ---")
    print("Time:", datetime.utcnow().isoformat())
    print("Payload:", json.dumps(payload, indent=2))
    print("------------------------\n")

    # 4) Respond FAST to keep their system happy
    return JSONResponse({"status": "ok", "message": "Data received successfully"})