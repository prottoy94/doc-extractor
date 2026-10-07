import json
import random
from datetime import date
from datetime import timedelta
from pathlib import Path

import numpy
from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageFont

from app import config


RANDOM_SEED = 42
NUMBER_OF_RECEIPTS = 150
NUMBER_OF_PAYMENTS = 150
OUTPUT_FOLDER = Path("data") / "synthetic"

RECEIPT_CHARACTERS_PER_LINE = 30
RECEIPT_FONT_SIZE = 30
RECEIPT_LINE_HEIGHT = 46
RECEIPT_MARGIN = 30
PHOTO_TABLE_PADDING = 60
SCAN_PROBABILITY = 0.3

PAYMENT_MIN_WIDTH = 540
PAYMENT_MARGIN = 36
PAYMENT_LINE_HEIGHT = 64
PAYMENT_HEADER_FONT_SIZE = 40
PAYMENT_BODY_FONT_SIZES = [26, 30, 34]
DARK_MODE_PROBABILITY = 0.5

MONO_FONT_FILE_NAMES = [
    "cour.ttf",
    "Courier New.ttf",
    "DejaVuSansMono.ttf",
    "LiberationMono-Regular.ttf",
]
SANS_FONT_FILE_NAMES = [
    "arial.ttf",
    "Arial.ttf",
    "DejaVuSans.ttf",
    "LiberationSans-Regular.ttf",
]

SHOP_NAMES = [
    "Green Valley Mart",
    "Rahim Store",
    "Karim Traders",
    "City Fresh Bazar",
    "Sunrise Pharmacy",
    "Noor Grocery",
    "Delta Super Shop",
    "Lake View Mart",
    "Star Kitchen Market",
    "Metro Daily Needs",
]

ITEMS = [
    ("Rice 5kg", 550, 750),
    ("Cooking Oil 1L", 170, 220),
    ("Sugar 1kg", 110, 140),
    ("Tea 200g", 90, 160),
    ("Milk 1L", 80, 110),
    ("Eggs 12pcs", 120, 160),
    ("Lentils 1kg", 120, 170),
    ("Flour 2kg", 100, 150),
    ("Soap", 40, 90),
    ("Biscuits", 20, 60),
]

RECEIPT_REFERENCE_LABELS = ["Invoice No:", "Receipt No:"]
RECEIPT_TOTAL_LABELS = ["Total:", "Grand Total:", "Total Amount:"]
PAYMENT_SHOP_LABELS = ["Paid to:", "Merchant:"]
PAYMENT_REFERENCE_LABELS = ["Transaction ID:", "TrxID:"]
PAYMENT_TOTAL_LABELS = ["Amount:", "Total Amount:"]

TRANSACTION_ID_CHARACTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def load_font(font_file_names, font_size):
    for font_file_name in font_file_names:
        try:
            return ImageFont.truetype(font_file_name, font_size)
        except OSError:
            continue
    return ImageFont.load_default(font_size)


def make_random_date():
    first_day = date(2024, 1, 1)
    number_of_days = random.randint(0, 900)
    return first_day + timedelta(days=number_of_days)


def format_money(amount):
    return "{:.2f}".format(amount)


def make_transaction_id():
    transaction_id = ""
    for position in range(10):
        transaction_id = transaction_id + random.choice(TRANSACTION_ID_CHARACTERS)
    return transaction_id


def make_receipt_content():
    shop_name = random.choice(SHOP_NAMES).upper()
    reference_no = "INV-" + str(random.randint(10000, 99999))
    date_value = make_random_date()
    date_format = random.choice(config.DATE_FORMATS)
    number_of_items = random.randint(2, 5)
    chosen_items = random.sample(ITEMS, number_of_items)

    lines = []
    lines.append(shop_name)
    lines.append(random.choice(RECEIPT_REFERENCE_LABELS) + " " + reference_no)
    lines.append("Date: " + date_value.strftime(date_format))

    total_amount = 0
    for item in chosen_items:
        item_name = item[0]
        lowest_price = item[1]
        highest_price = item[2]
        price = random.randint(lowest_price, highest_price)
        total_amount = total_amount + price
        lines.append(item_name.ljust(20) + format_money(price).rjust(10))

    total_text = format_money(total_amount)
    total_label = random.choice(RECEIPT_TOTAL_LABELS)
    lines.append(total_label.ljust(20) + total_text.rjust(10))

    fields = {
        "shop_name": shop_name,
        "reference_no": reference_no,
        "date": date_value.isoformat(),
        "total": total_text,
    }
    return {"template": "receipt", "lines": lines, "fields": fields}


def make_payment_content():
    shop_name = random.choice(SHOP_NAMES)
    transaction_id = make_transaction_id()
    date_value = make_random_date()
    date_format = random.choice(config.DATE_FORMATS)
    total_text = format_money(random.randint(50, 5000))

    lines = []
    lines.append("Payment Successful")
    lines.append(random.choice(PAYMENT_SHOP_LABELS) + " " + shop_name)
    lines.append(random.choice(PAYMENT_REFERENCE_LABELS) + " " + transaction_id)
    lines.append("Date: " + date_value.strftime(date_format))
    lines.append(random.choice(PAYMENT_TOTAL_LABELS) + " " + total_text)
    lines.append("Thank you for using our service")

    fields = {
        "shop_name": shop_name,
        "reference_no": transaction_id,
        "date": date_value.isoformat(),
        "total": total_text,
    }
    return {"template": "payment", "lines": lines, "fields": fields}


def draw_receipt_image(lines):
    font = load_font(MONO_FONT_FILE_NAMES, RECEIPT_FONT_SIZE)
    text_width = int(font.getlength("M" * RECEIPT_CHARACTERS_PER_LINE))
    image_width = text_width + 2 * RECEIPT_MARGIN
    image_height = len(lines) * RECEIPT_LINE_HEIGHT + 2 * RECEIPT_MARGIN

    image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
    drawing = ImageDraw.Draw(image)

    y_position = RECEIPT_MARGIN
    for line in lines:
        drawing.text(
            (RECEIPT_MARGIN, y_position), line, font=font, fill=(20, 20, 20)
        )
        y_position = y_position + RECEIPT_LINE_HEIGHT
    return image


def draw_payment_image(lines, dark_mode):
    if dark_mode:
        background_color = (24, 24, 28)
        text_color = (235, 235, 235)
        header_color = (80, 220, 140)
    else:
        background_color = (255, 255, 255)
        text_color = (30, 30, 30)
        header_color = (0, 140, 80)

    header_font = load_font(SANS_FONT_FILE_NAMES, PAYMENT_HEADER_FONT_SIZE)
    body_font_size = random.choice(PAYMENT_BODY_FONT_SIZES)
    body_font = load_font(SANS_FONT_FILE_NAMES, body_font_size)

    body_lines = lines[1:]
    widest_line = 0
    for line in body_lines:
        line_width = body_font.getlength(line)
        if line_width > widest_line:
            widest_line = line_width

    image_width = max(PAYMENT_MIN_WIDTH, int(widest_line) + 2 * PAYMENT_MARGIN)
    image_height = (
        2 * PAYMENT_MARGIN
        + PAYMENT_LINE_HEIGHT
        + 30
        + len(body_lines) * PAYMENT_LINE_HEIGHT
    )

    image = Image.new("RGB", (image_width, image_height), background_color)
    drawing = ImageDraw.Draw(image)

    y_position = PAYMENT_MARGIN
    drawing.text(
        (PAYMENT_MARGIN, y_position), lines[0], font=header_font, fill=header_color
    )
    y_position = y_position + PAYMENT_LINE_HEIGHT + 30

    for line in body_lines:
        drawing.text(
            (PAYMENT_MARGIN, y_position), line, font=body_font, fill=text_color
        )
        y_position = y_position + PAYMENT_LINE_HEIGHT
    return image


def add_noise(image, strength):
    pixel_array = numpy.array(image, dtype=numpy.float32)
    random_noise = numpy.random.normal(0, strength, pixel_array.shape)
    noisy_array = pixel_array + random_noise
    noisy_array = numpy.clip(noisy_array, 0, 255)
    noisy_array = noisy_array.astype(numpy.uint8)
    return Image.fromarray(noisy_array)


def make_photo_look(receipt_image):
    table_color = (
        random.randint(70, 130),
        random.randint(60, 110),
        random.randint(50, 100),
    )
    canvas_width = receipt_image.width + 2 * PHOTO_TABLE_PADDING
    canvas_height = receipt_image.height + 2 * PHOTO_TABLE_PADDING

    canvas = Image.new("RGB", (canvas_width, canvas_height), table_color)
    canvas.paste(receipt_image, (PHOTO_TABLE_PADDING, PHOTO_TABLE_PADDING))

    tilt_angle = random.uniform(-6, 6)
    canvas = canvas.rotate(
        tilt_angle,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=table_color,
    )

    brightness_factor = random.uniform(0.65, 1.0)
    canvas = ImageEnhance.Brightness(canvas).enhance(brightness_factor)

    blur_radius = random.uniform(0.3, 1.3)
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    noise_strength = random.uniform(4, 14)
    canvas = add_noise(canvas, noise_strength)
    return canvas


def save_example(image, content, file_stem, extension, condition):
    image_file_name = file_stem + extension
    image_path = OUTPUT_FOLDER / image_file_name

    if extension == ".jpg":
        image.save(image_path, "JPEG", quality=random.randint(45, 85))
    else:
        image.save(image_path, "PNG")

    answer = {
        "image_file": image_file_name,
        "template": content["template"],
        "condition": condition,
        "text": "\n".join(content["lines"]),
        "fields": content["fields"],
    }
    answer_path = OUTPUT_FOLDER / (file_stem + ".json")
    with open(answer_path, "w", encoding="utf-8") as answer_file:
        json.dump(answer, answer_file, indent=2, ensure_ascii=False)


def make_one_receipt(number):
    content = make_receipt_content()
    receipt_image = draw_receipt_image(content["lines"])
    file_stem = "receipt_" + str(number).zfill(4)

    if random.random() < SCAN_PROBABILITY:
        condition = "scan"
        final_image = receipt_image
        extension = ".png"
    else:
        condition = "photo"
        final_image = make_photo_look(receipt_image)
        extension = ".jpg"

    save_example(final_image, content, file_stem, extension, condition)


def make_one_payment(number):
    content = make_payment_content()
    dark_mode = random.random() < DARK_MODE_PROBABILITY
    payment_image = draw_payment_image(content["lines"], dark_mode)
    file_stem = "payment_" + str(number).zfill(4)

    if dark_mode:
        condition = "screenshot_dark"
    else:
        condition = "screenshot_light"

    save_example(payment_image, content, file_stem, ".png", condition)


def main():
    random.seed(RANDOM_SEED)
    numpy.random.seed(RANDOM_SEED)
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    for number in range(1, NUMBER_OF_RECEIPTS + 1):
        make_one_receipt(number)
    print("Created", NUMBER_OF_RECEIPTS, "receipts")

    for number in range(1, NUMBER_OF_PAYMENTS + 1):
        make_one_payment(number)
    print("Created", NUMBER_OF_PAYMENTS, "payment screenshots")

    print("Files are in:", OUTPUT_FOLDER)


if __name__ == "__main__":
    main()
