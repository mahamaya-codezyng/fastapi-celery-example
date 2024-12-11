from celery_app import celery_app  # Use the existing Celery app
from openai import AzureOpenAI
import os
import json

# DALL-E client setup
client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint=os.getenv("DALLE_TARGET_URI"),
    api_key=os.getenv("OPENAI_API_KEY"),
)


@celery_app.task
def generate_image(item: str):
        print(f"task initiated for {item}")
        prompt = f"""
        Generate a high-quality, realistic photograph of the item mentioned below on a plain white background. Only one item should appear in the image, captured in a straightforward, well-lit view to clearly display its color, style, pattern and details.{item}
        """

        # Call OpenAI DALL-E endpoint
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1
        )
        image_url = json.loads(response.model_dump_json())['data'][0]['url']
        print(f"image url {image_url}")
        return image_url
