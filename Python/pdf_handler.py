import fitz  # PyMuPDF
import re
import json
import pandas

import pdfplumber

# Load the PDF
doc = fitz.open("Mamud Hasan.pdf.pdf")
text = "\n".join(page.get_text() for page in doc)

print(text)

# Define section headers
headers = ["EDUCATION", "SKILLS", "CERTIFICATION", "TECHNICAL SKILLS", "PROFILE SUMMARY", "RELEVANT WORK EXPERIENCE", "EMPLOYMENT HISTORY"]

# Build regex pattern to find sections
pattern = "|".join([re.escape(h) for h in headers])

print(f"pattern:\n {pattern}")
matches = list(re.finditer(pattern, text, re.IGNORECASE))
print(f"matches:\n {matches}")
# Extract SKILLS section
skills_text = ""
for i, match in enumerate(matches):
    if match.group().upper() == "SKILLS":
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        skills_text = text[start:end].strip()
        break

# Output the SKILLS section
print("--- SKILLS SECTION ---")
print(skills_text)



with pdfplumber.open("Mamud Hasan.pdf.pdf") as pdf:
    for page in pdf.pages:
        for rect in page.rects:  # detects boxes/borders
            print("Box:", rect)
        # text = page.extract_text()
        # print(text)
        
box = {
    "x0": 0.0,
    "y0": -7.9200062999999545,
    "x1": 611.0,
    "y1": 784.0
}

with pdfplumber.open("Mamud Hasan.pdf.pdf") as pdf:
    page = pdf.pages[1]  # Page numbers are 0-indexed
    cropped = page.crop((box["x0"], box["y0"], box["x1"], box["y1"]))
    text_in_box = cropped.extract_text()
    print("--- Text inside the box ---")
    print(text_in_box)

with pdfplumber.open("Mamud Hasan.pdf.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        print(f"\n--- Page {page_num} ---")
        for i, rect in enumerate(page.rects, start=1):
            print(f"Box {i}:")
            print({
                "page": page_num,
                "x0": rect["x0"],
                "y0": rect["y0"],
                "x1": rect["x1"],
                "y1": rect["y1"],
                "width": rect["width"],
                "height": rect["height"],
                "fill_color": rect.get("non_stroking_color"),
                "stroke_color": rect.get("stroking_color")
            })

print(f"\n--------- Table Extraction ---")
with pdfplumber.open("Mamud Hasan.pdf.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        for table_index, table in enumerate(tables, start=1):
            print(f"\n--- Page {page_num}, Table {table_index} ---")
            for row in table:
                print(row)