APP_NAME = "Document Field Extractor"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = (
    "Reads a photo or screenshot of a receipt or bill, "
    "fills a form with the extracted values, and saves it."
)

ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png"]
MAX_UPLOAD_MEGABYTES = 10
MAX_UPLOAD_BYTES = MAX_UPLOAD_MEGABYTES * 1024 * 1024

MAX_IMAGE_SIDE_PIXELS = 2000
DARK_BACKGROUND_BRIGHTNESS = 127
MIN_SKEW_DEGREES = 0.5

OCR_LANGUAGE = "eng"
TESSERACT_COMMAND = None

FORM_FIELD_NAMES = ["shop_name", "reference_no", "date", "total"]
FIELD_KEYWORDS = {
    "shop_name": ["merchant", "paid to", "shop name"],
    "reference_no": [
        "invoice no",
        "invoice",
        "receipt no",
        "transaction id",
        "trxid",
        "ref",
    ],
    "date": ["date"],
    "total": ["grand total", "total amount", "total", "amount", "net payable"],
}

DATE_FORMATS = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d %b %Y",
]

LABEL_MATCH_MIN_SIMILARITY = 0.75 # This will eventually be used for fuzzy matching.
# 0.75 means we require approximately 75% similarity or higher before considering the match acceptable.
REVIEW_CONFIDENCE_THRESHOLD = 0.75 # If the system isn't sure about a value, mark it "please check".
# 0.75 means we require approximately 75% confidence or higher before considering the value acceptable.

DATABASE_URL = "sqlite:///records.db"
STORE_IMAGES = False
