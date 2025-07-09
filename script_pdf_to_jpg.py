import os
from datetime import datetime, timedelta
from pdf2image import convert_from_path

# --- Inputs ---
pdf_path = input("Enter the path to the PDF file: ").strip()
start_page = int(input("Enter the start page (inclusive): ").strip())
end_page = int(input("Enter the end page (inclusive): ").strip())

# --- Folder setup ---
tomorrow = datetime.now() + timedelta(days=1)
base_folder = os.path.join("pages", tomorrow.strftime("%d-%m-%Y"))
images_folder = os.path.join(base_folder, "images")

os.makedirs(images_folder, exist_ok=True)

# Extract first page as cover.jpg
cover_image = convert_from_path(
    pdf_path,
    dpi=200,
    first_page=1,
    last_page=1,
    fmt='jpeg'
)[0]
cover_path = os.path.join(images_folder, "cover.jpg")
cover_image.save(cover_path, "JPEG")
print(f"✅ Cover saved as {cover_path}")

# --- Convert PDF pages ---
images = convert_from_path(
    pdf_path,
    dpi=200,
    first_page=start_page,
    last_page=end_page,
    fmt='jpeg'
)

# --- Save images inside the images/ folder ---
for i, img in enumerate(images):
    page_num = start_page + i
    img_path = os.path.join(images_folder, f"page_{page_num}.jpg")
    img.save(img_path, "JPEG")

print(f"✅ Images saved inside {images_folder}")

# --- Create index.html ---
html_path = os.path.join(base_folder, "index.html")

with open(html_path, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PDF Pages Viewer</title>
  <style>
    body {
      background: #f4f4f4;
      font-family: sans-serif;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
    }
    img {
      width: 100%; 
      height: auto;
      margin: 10px; 
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
      border-radius: 10px;
    }
  </style>
</head>
<body>
""")
    # Add images referencing the images/ subfolder
    for i in range(len(images)):
        page_num = start_page + i
        f.write(f'  <img src="images/page_{page_num}.jpg" alt="Page {page_num}">\n')

    f.write("""
</body>
</html>
""")

print(f"✅ index.html created at {html_path}")
