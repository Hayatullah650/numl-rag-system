
from pathlib import Path
from io import BytesIO
import shutil
import pymupdf
import pytesseract
from PIL import Image

DATA_DIR = Path("data")
MIN_TEXT_LENGTH = 80

if not shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


def extract_page_text(page):
    text = page.get_text("text").strip()

    if len(text) >= MIN_TEXT_LENGTH:
        return text

    if not shutil.which("tesseract") and not Path(
        pytesseract.pytesseract.tesseract_cmd
    ).exists():
        print("Tesseract OCR is not installed.")
        return text

    try:
        pixmap = page.get_pixmap(dpi=300, alpha=False)
        image = Image.open(BytesIO(pixmap.tobytes("png")))
        ocr_text = pytesseract.image_to_string(image).strip()

        return ocr_text if len(ocr_text) > len(text) else text
    except Exception as error:
        print(f"OCR failed on page {page.number + 1}: {error}")
        return text


def ingest_pdfs():
    documents = []
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the data folder.")
        return documents

    for pdf_path in pdf_files:
        try:
            with pymupdf.open(pdf_path) as pdf:
                extracted_pages = 0

                for page_number, page in enumerate(pdf, start=1):
                    text = extract_page_text(page)

                    if text:
                        documents.append({
                            "text": text,
                            "source": pdf_path.name,
                            "page": page_number
                        })
                        extracted_pages += 1

                print(
                    f"Processed: {pdf_path.name} "
                    f"({extracted_pages}/{len(pdf)} pages)"
                )

        except Exception as error:
            print(f"Failed: {pdf_path.name} — {error}")

    print(f"\nPDF files found: {len(pdf_files)}")
    print(f"Pages with extracted text: {len(documents)}")

    return documents


if __name__ == "__main__":
    pages = ingest_pdfs()

    if pages:
        print("\nFirst extracted page:")
        print(pages[0]["text"][:500])
        print(f"\nSource: {pages[0]['source']}")
        print(f"Page: {pages[0]['page']}")
