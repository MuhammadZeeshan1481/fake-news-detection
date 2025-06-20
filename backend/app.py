from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import requests
import os
import sqlite3
import json
from utils.explain import extract_attention_words  # Make sure path is correct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model/saved_model")

# Load Model + Tokenizer
try:
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model.eval()
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print("Failed to load model/tokenizer:", e)

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "../database/predictions.db"))
NEWS_API_KEY = "9e646486adb84a8ba7b87a4db20372d6"  # Demo key

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.post("/predict")
async def predict_news(input: InputText):
    try:
        # Prediction
        inputs = tokenizer(input.text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)
            prediction = torch.argmax(probs).item()
            confidence = float(probs[0][prediction]) * 100

        # Attention words
        suspicious_words = extract_attention_words(model, tokenizer, input.text)

        # Log to DB
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO predictions (input_text, prediction, confidence, suspicious_words) VALUES (?, ?, ?, ?)",
                (
                    input.text,
                    "Real" if prediction == 1 else "Fake",
                    round(confidence, 2),
                    json.dumps(suspicious_words)
                )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print("DB logging error:", e)

        return {
            "prediction": "Real" if prediction == 1 else "Fake",
            "confidence": round(confidence, 2),
            "suspicious_words": suspicious_words
        }

    except Exception as e:
        print("Prediction Error:", e)
        return {"error": "Prediction failed", "details": str(e)}

@app.post("/verify")
async def verify_news(input: InputText):
    try:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={input.text}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        )
        response = requests.get(url)
        data = response.json()
        if data.get("status") != "ok":
            return {"verified": False, "error": "NewsAPI error"}
        articles = data.get("articles", [])[:3]
        sources = [a["source"]["name"] for a in articles]
        titles = [a["title"] for a in articles]
        return {
            "verified": len(articles) > 0,
            "matched_sources": sources,
            "matched_titles": titles
        }
    except Exception as e:
        print("Verification Error:", e)
        return {"error": "Verification failed", "details": str(e)}
