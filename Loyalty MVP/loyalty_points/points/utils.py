import pytesseract
import re
import hashlib
from .models import Store

def extract_info(image_path):
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    text = pytesseract.image_to_string(image_path)
    
    stores = Store.objects.values_list('name', flat=True)
    price_patterns = [
        r'\s+TOTAL\s+(\d+\.\d+)',
        r'TOTAL\s+\d+\s+(\d+\.\d+)',
        r'TOTAL\s+(\d+\.\d+)'
    ]
    date_patterns = [
        r'(\d{2}/\d{2}/\d{2})',
        r'(\d{2}/\d{2}/\d{4})'
    ]

    total_price = "Unknown"
    extracted_date = "Unknown"
    store_name = "Unknown"

    # Extract the price
    for pattern in price_patterns:
        match = re.search(pattern, text)
        if match:
            total_price = match.group(1)
            break

    # Extract the store name
    for store in stores:
        pattern = re.compile(r'\b{}\b'.format(re.escape(store)), re.IGNORECASE)
        if re.search(pattern, text):
            store_name = store
            break

    for date in date_patterns:
        match = re.search(date, text)
        if match:
            extracted_date = match.group(1)

    return store_name, extracted_date, total_price


def generate_image_identifier(image_content):
    image_hash = hashlib.sha256(image_content).hexdigest()
    return image_hash