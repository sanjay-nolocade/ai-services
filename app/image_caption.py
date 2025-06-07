# app/image_caption.py
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import torch
import io

# Load model ONCE at startup
model_name = "nlpconnect/vit-gpt2-image-captioning"
print("🔹 Loading model:", model_name)
model = VisionEncoderDecoderModel.from_pretrained(model_name)
feature_extractor = ViTImageProcessor.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"✅ Model loaded on {device}")

async def generate_image_captions(file, num_captions=3) -> list:
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # 🚀 Use sampling (safe for multiple captions)
    output_ids = model.generate(
        pixel_values,
        max_length=16,
        do_sample=True,
        temperature=1.0,
        top_k=50,
        num_return_sequences=num_captions
    )

    captions = [tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]
    return captions