"""Main module to process OCR using Gemini model."""

import logging
import os
from google import genai
from utils import gemini_key, utils
import argparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def process_ocr(path: str = '../archivos', 
                model_id: str ="gemini-2.5-flash", 
                clients: list = [genai.Client(api_key=k) for k in gemini_key.gemini_api_key]) -> None:
    """
    Process OCR on the image using Gemini model.

    Args:
        path (str): path to the image file.
        model_id (str): Gemini model ID.
        clients (list): list of Google clients.
    """

    result = []
    for file in os.listdir(path):
        if file.endswith(".jpeg"):
            logger.info(f"Processing file: {file}")
            # load image and converse
            img_left, img_rigth = utils.load_image(path = os.path.join(path, file))
            # first interaction (left)
            response: str = utils.converse_image_and_text_gemini(google_clients = clients,
                                                        model_id=model_id,
                                                        input_image = img_left)
            result.append(utils.process_response(response))

            # second interaction (right)
            response: str = utils.converse_image_and_text_gemini(google_clients = clients,
                                                        model_id=model_id,
                                                        input_image = img_rigth)
            result.append(utils.process_response(response))

    result = sum(result, [])
    utils.save_response(result)


if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="Proceso OCR")
    #
    #parser.add_argument(
    #    "--path",
    #    type=str,
    #    required=False,
    #    help="Ruta a la carpeta de archivos"
    #)
    #parser.add_argument(
    #    "--model_id",
    #    type=str,
    #    required=False,
    #    help="ID del modelo"
    #)
    #parser.add_argument(
    #    "--clients",
    #    nargs="+",
    #    required=False,
    #    help="Lista de clientes"
    #)
#
    #args = parser.parse_args()
#
    #process_ocr(
    #    path=args.path,
    #    model_id=args.model_id,
    #    clients=args.clients
    #)
    process_ocr()