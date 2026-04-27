import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")
POPPLER_PATH = os.getenv("POPPLER_PATH")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

INPUT_FILE = DATA_DIR / "sample_statement.pdf"
OUTPUT_FILE = DATA_DIR / "raw_text.txt"


def ocr_from_pdf(pdf_path: Path) -> str:
    pages = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    full_text = ""
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        full_text += f"\n\n--- Page {i+1} ---\n{text}"

    return full_text


def main():
    text = ocr_from_pdf(INPUT_FILE)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    print("OCR complete. Text saved.")


if __name__ == "__main__":
    main()