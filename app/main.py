# app/main.py
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from app.image_caption import generate_image_captions
from typing import Dict

app = FastAPI(
    title="AI Image Alt Text Generator API",
    description="Generates multiple descriptive alt texts for images using ViT-GPT2",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc",
)

# Allow CORS for your Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-alt-text/", summary="Generate Multiple Alt Texts", description="Upload an image and get multiple alt text suggestions.")
async def generate_alt_text(file: UploadFile = File(...), num_captions: int = Query(3, ge=1, le=10)) -> Dict[str, list]:
    captions = await generate_image_captions(file, num_captions)
    return {"alt_texts": captions}