"""Utility functions for image and text processing with Gemini models."""

import pandas as pd
import numpy as np
from PIL import Image
import logging
import io
import os
import time
import random
import json

from google import genai
from google.genai import types

import matplotlib.pyplot as plt
import seaborn as sns

import utils.prompt as prompt

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def load_image(path: str) -> list[bytes]:
    """Load image from path
    
    Args: 
        path (str): image path
        image_valid (bool): True if image path is valid

    Returns:
        list[bytes], images bytes
    """
    try:
        # process image and split
        img: Image = Image.open(path)
        img: Image = img.convert("RGB")
    
        ancho, alto = img.size
        mitad = ancho // 2
        left: Image = img.crop((0, 0, mitad, alto))
        rigth: Image = img.crop((mitad, 0, ancho, alto))
    
        # convert bytes
        buffer_left = io.BytesIO()
        left.save(buffer_left, format="JPEG")  # or PNG
        bytes_left: bytes = buffer_left.getvalue()
        # optimize image if necessary
        bytes_left: bytes = optimize_image(data=bytes_left)
    
        buffer_rigth = io.BytesIO()
        rigth.save(buffer_rigth, format="JPEG")
        bytes_rigth: bytes = buffer_rigth.getvalue()
        # optimize image if necessary
        bytes_rigth: bytes = optimize_image(data=bytes_rigth)

        return [bytes_left, bytes_rigth]

    except:
        logger.error("Error processing image: %s", path)
        return None
    
def optimize_image(data: bytes, max_bytes: float = 4.5) -> bytes:
    """
    Si una imagen supera los 4MB, la comprime hasta que cumpla el límite.

    Args:
        data (bytes): image bytes
        max_bytes (float): max MB allowed to process image

    Returns:
        bytes: reduzed image bytes.
    """

    max_bytes: int = max_bytes * 1024 * 1024

    if len(data) <= max_bytes:
        logger.info('Return without resize.')
        return data

    img = Image.open(io.BytesIO(data))
    buffer = io.BytesIO()

    quality = 90
    while len(data) > max_bytes and quality > 10:
        logger.info('Optimize quality.')
        buffer = io.BytesIO()
        img.save(buffer, format="PNG", quality=quality)
        data = buffer.getvalue()
        quality -= 10

    if len(data) > max_bytes:
        logger.info('Optimize resolution.')
        w, h = img.size
        factor = 0.9
        while len(data) > max_bytes and w > 200 and h > 200:
            w = int(w * factor)
            h = int(h * factor)
            img_resized = img.resize((w, h))

            buffer = io.BytesIO()
            img_resized.save(buffer, format="PNG", quality=70)
            data = buffer.getvalue()

    return data


def add_text_context() -> str:
    """
    Adds context to the input text.
    Returns:
        context (str): context to add to the input text.
    """

    return prompt.prompt

def converse_image_and_text_gemini(google_clients: list,
                                    model_id: str,
                                    input_image: bytes) -> str:
    """
    Sends a message to a model.
    Args:
        google_clients (list[genai.client]): list with genai clients.
        model_id (str): The model ID to use.
        input text (str): The input message.

    Returns:
        response (str): response that the model generated.
    """


    image = types.Part.from_bytes(
        data=input_image, mime_type="image/jpeg"
    )

    text: str = add_text_context()

    contents = [image, text]
    
    random.shuffle(google_clients)
    for client in google_clients:
        for attempt in range(3):   # 3 reintentos por clave
            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=contents
                )

                logger.info(f"Successful response from image and text with model {model_id}")
                return response.text
            except Exception:

                logger.error(f"Error with key in {model_id}. Retry")
                time.sleep(0.5 * (2 ** attempt) + random.random() * 0.2)

    return "MODEL ERROR"

def process_response(response: str) -> json:
    """Extracts and formats the JSON array from the model response.
    
    Args:
        response (str): The raw response string from the model.

    Returns:
        data (json): Extracted JSON data.
    """
    start = response.find('[')
    end = response.rfind(']') + 1
    json_string = response[start:end]
    data = json.loads(json_string)
    return data

def save_response(result: json) -> None:
    """Saves the model response to an Excel file.
    Args:
        result (json): The JSON data to save.
    """
    date = time.strftime("%Y%m%d_%H%M%S")
    df = pd.DataFrame(result)
    df.to_excel(f"../cuestionario_{date}.xlsx", index=False)

    logger.info(f"Response saved to cuestionario_{date}.xlsx")