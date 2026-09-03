import os
import time
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=API_KEY)

def decide_action(transaction):
    prompt = f"""A payment failed with these details:
- Amount: Rs.{transaction['amount']}
- Failure reason: {transaction['reason']}
- Payment method: {transaction['method']}

Decide the best recovery action. Reply in EXACTLY this format:
ACTION: <RETRY or SEND_MESSAGE or ESCALATE>
REASON: <one short sentence why>"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )
            text = response.text.strip()

            action_line = [l for l in text.split("\n") if l.startswith("ACTION:")][0]
            reason_line = [l for l in text.split("\n") if l.startswith("REASON:")][0]

            action = action_line.replace("ACTION:", "").strip()
            reason = reason_line.replace("REASON:", "").strip()
            return action, reason

        except Exception as e:
            print(f"ERROR on attempt {attempt}: {e}")
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            return ("SEND_MESSAGE", f"Gemini temporarily unavailable ({str(e)[:100]}) - used fallback.")