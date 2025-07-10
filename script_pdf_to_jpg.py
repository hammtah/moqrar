import os
from datetime import datetime, timedelta
from pdf2image import convert_from_path
import json
import shutil

# --- Inputs ---
pdf_path = input("Enter the path to the PDF file: ").strip()
start_page = int(input("Enter the start page (inclusive): ").strip())
end_page = int(input("Enter the end page (inclusive): ").strip())
# name = input("Enter the name for the entry: ").strip()
name = "(رقائق القرآن( ٦٧ - ٩٤"
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
    #progress-bar-container {
      position: fixed;
      left: 8px;
      bottom: 0;
      width: calc(100% - 16px);
      height: 8px;
      background: rgba(0,0,0,0.08);
      z-index: 1000;
    }
    #progress-bar {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #2dc27c, #2de891);
      border-radius: 8px;
      transition: width 0.2s;
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
  <div id="progress-bar-container">
    <div id="progress-bar"></div>
    <div id="progress-tooltip" style="position:absolute;left:0;transform:translateY(-120%);bottom:-150%;background:#222;color:#fff;padding:4px 8px;border-radius:6px;font-size:12px;white-space:nowrap;pointer-events:none;z-index:1002;">0%</div>
  </div>
  <!-- Quiz Button -->
  <div style="width:100%;display:flex;justify-content:center;margin:24px 0 16px 0;position:relative;z-index:1001;">
    <a href="quiz.html" style="background:linear-gradient(90deg,#2dc27c,#2de891);color:white;padding:16px 32px;border:none;border-radius:8px;font-size:1.2em;font-weight:bold;text-decoration:none;box-shadow:0 2px 8px rgba(0,0,0,0.15);transition:background 0.2s;cursor:pointer;">Take the Quiz</a>
  </div>
  <script type="module" src="/progress.js"></script>
</body>
</html>
""")

print(f"✅ index.html created at {html_path}")

shutil.copy("quiz.html", os.path.join(base_folder, "quiz.html"))
print(f"✅ quiz.html copied to {base_folder}")
# Construct the moqrar object
moqrar = {
    "name": name,
    "url": os.path.join("pages", tomorrow.strftime("%d-%m-%Y"), "index.html").replace("\\", "/"),
    "image": os.path.join("pages", tomorrow.strftime("%d-%m-%Y"), "images", "cover.jpg").replace("\\", "/"),
    "date": tomorrow.strftime("%d-%m-%Y"),
    "completed": False,
    "progress": 0
}
# Push to Firebase
# doc_ref = db.collection("moqrarat").add(moqrar)
# print("✅ Uploaded to Firebase")

# Path to data.json (assuming it is in the current working directory)
data_json_path = "data.json"

# Read existing data or initialize empty list
if os.path.exists(data_json_path):
    with open(data_json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
        except json.JSONDecodeError:
            data = []
else:
    data = []

# Append the new entry
data.append(moqrar)

# Write back to data.json
with open(data_json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"✅ Added new entry to {data_json_path}")