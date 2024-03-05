import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import os

# Set the path to tesseract.exe in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path accordingly


def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.convert('L')
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.point(lambda p: p > 128 and 255)
    img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
    return img


def image_to_text(image_path):
    img = preprocess_image(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text


def post_process_to_dataframe(raw_text):
    lines = raw_text.split('\n')
    rows = []
    for line in lines:
        cells = line.split('  ')
        cells = [cell.strip() for cell in cells if cell.strip()]
        if cells:
            rows.append(cells)
    return rows


def save_to_text_file(rows):
    with open('output.txt', 'w', encoding='utf-8') as file:
        for row in rows:
            file.write(' '.join(row) + '\n')


def select_image_and_convert():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    extracted_text = image_to_text(file_path)
    rows = post_process_to_dataframe(extracted_text)
    save_to_text_file(rows)

    status_label.config(text="Text has been extracted and saved to output.txt")


def open_output_file():
    os.system("start output.txt")


root = tk.Tk()
root.title("Image to Text Converter")
root.configure(bg="blue")

title_label = tk.Label(root, text="PICT => .TXT", font=("Comic Sans", 24, "bold"), bg="blue", fg="white")
title_label.pack(pady=20)

status_label = tk.Label(root, text="Select an image to extract text", bg="blue", fg="white")
status_label.pack(pady=20, expand=True)

button_frame = tk.Frame(root, bg="blue")
button_frame.pack(side=tk.BOTTOM, pady=20)

select_button = tk.Button(button_frame, text="Select Image", command=select_image_and_convert)
select_button.pack(side=tk.LEFT, padx=10)

open_button = tk.Button(button_frame, text="Open Extracted Text", command=open_output_file)
open_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
