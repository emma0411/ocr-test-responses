# OCR process

This project aims to process OCR for questionnaires with circles. It processes all the images and saves them in an Excel file containing three columns: question number, question, and result.

# 🗂️ Document

The program requires documents in `.jpeg` format. Files should be placed in the `archivos` folder.

## ⚒️ Installation

You need python>=3.9. Run this command in the terminal from the project root:

```
pip install -r requirements.txt
```

### ⚠️ Prerequisites

You need a Google Generative AI API key (`genai key`) to use this project.  
Create a file named `gemini_key.py` and add your key as follows:

```python
gemini_api_key = ["YOUR_GENAI_API_KEY"]
```

## 🚀 Usage

To run the program:

```
python project/main.py
```

## 📁 Project Structure

- `main.py`: Main script to run the OCR process.
- `archivos/`: Folder for `.jpeg` files to be processed.
- `project/``: Project main folder
    - `requirements.txt`: Project dependencies. 
    - `main.py`: Main script to run the OCR process.
    - `utils/`: Helper functions for OCR processing.
    - `README.md`: Project documentation.

## 📝 Example

Place your images in the `archivos` folder and run the command above. The result will be saved according to the script configuration.

```
import logging
import os
from google import genai
from utils import gemini_key
import main

# configure genai clients
clients = [genai.Client(api_key=k) for k in gemini_key.gemini_api_key]
#model_id = "gemini-2.5-pro"
model_id = "gemini-2.5-flash"

# process images in the folder
main.process_ocr(path = '../archivos', model_id = model_id, clients = clients)
```

## 🤝 Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.

---
Developed with ♥️ by Emma