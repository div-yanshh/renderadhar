# # # from flask import Flask, request, render_template, send_file, redirect, url_for , jsonify
# # # import os
# # # from werkzeug.utils import secure_filename
# # # import pdf2image
# # # import fitz
# # # from PIL import Image, ImageDraw
# # # import easyocr
# # # import re
# # # import cv2
# # # import numpy as np
# # # import uuid
# # # import zipfile
# # # import csv 

# # # # Initialize Flask app
# # # app = Flask(__name__)
# # # USER_CREDENTIALS = {
# # #     "admin": "password123",  # Replace with your desired username and password
# # #     "user": "userpass"
# # # }
# # # # from flaskwebgui import FlaskUI
# # # # ui = FlaskUI(app)
# # # # Set upload and output directories
# # # UPLOAD_FOLDER = "uploads"
# # # PROCESSED_FOLDER = "processed"
# # # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # # os.makedirs(PROCESSED_FOLDER, exist_ok=True)  

# # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# # # active_uploads = {}

# # # # Helper functions
# # # def is_valid_12digit_number(text):
# # #     processed_text = re.sub(r'\D', '', text)
# # #     return len(processed_text) == 12

# # # def expand_bbox(bbox, padding=5):
# # #     top_left = (int(bbox[0][0] - padding), int(bbox[0][1] - padding))
# # #     bottom_right = (int(bbox[2][0] + padding), int(bbox[2][1] + padding))
# # #     return top_left, bottom_right



# # # def mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id):
# # #     doc = fitz.open(input_pdf_path)  # Open PDF document
# # #     reader = easyocr.Reader(['en'], gpu=False)
# # #     masked_pages = []
# # #     masked_numbers = []  # Collect all masked 12-digit numbers
# # #     masking_count = 0    # Count of maskings done
# # #     count = 0

# # #     pagestobefoundon = []

# # #     for page_num in range(len(doc)):
# # #         count += 1
# # #         page = doc.load_page(page_num)  # Load a single page
# # #         pix = page.get_pixmap(dpi=300)  # Render page as an image

# # #         # Convert pixmap to OpenCV format
# # #         img_cv = np.frombuffer(pix.tobytes(), np.uint8)
# # #         img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

# # #         if img_cv is None:
# # #             raise ValueError(f"Error decoding image data for page {count}")

# # #         # OCR processing
# # #         result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=5)

# # #         # Create an editable PIL image
# # #         img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
# # #         draw = ImageDraw.Draw(img_pil)

# # #         for bbox, text, score in result:
            

# # #             if is_valid_12digit_number(text):
# # #                 pagestobefoundon.append(count)
# # #                 top_left, bottom_right = expand_bbox(bbox)
# # #                 bbox_width = bottom_right[0] - top_left[0]
# # #                 adjusted_width = bbox_width * (8 / 12)
# # #                 adjusted_bottom_right = (top_left[0] + adjusted_width, bottom_right[1])
                
# # #                 draw.rectangle([top_left, adjusted_bottom_right], fill=(0, 0, 0))

# # #                 masked_numbers.append(text)
# # #                 masking_count += 1

# # #         # Save the modified image to the masked_pages list
# # #         img_pil = img_pil.convert("RGB")
# # #         masked_pages.append(img_pil)

# # #     # Save the masked pages back to a PDF
# # #     doc.close()
# # #     doc = fitz.open()  # Create a new PDF
# # #     for img in masked_pages:
# # #         # Save each page as a temporary image file
# # #         temp_img_path = f"{uuid.uuid4().hex}.png"
# # #         img.save(temp_img_path, format="PNG")

# # #         # Load the temporary image into a PDF page
# # #         imgdoc = fitz.open(temp_img_path)
# # #         pdfbytes = imgdoc.convert_to_pdf()
# # #         imgpdf = fitz.open("pdf", pdfbytes)
# # #         doc.insert_pdf(imgpdf)

# # #         # Clean up the temporary image
# # #         os.remove(temp_img_path)

# # #     doc.save(output_pdf_path)
# # #     doc.close()

# # #     return {
# # #         "file_name": os.path.basename(output_pdf_path),
# # #         "masking_count": masking_count,
# # #         "masked_numbers": masked_numbers,
# # #         "number_of_pages": len(masked_pages),
# # #         "masking_done_on_pages": pagestobefoundon
# # #     }



# # # def generate_summary_csv(summary_data, output_folder, session_id):
# # #     csv_filename = os.path.join(output_folder, f"Adhar Masking Summary.csv")
# # #     with open(csv_filename, mode='w', newline='') as csvfile:
# # #         writer = csv.DictWriter(csvfile, fieldnames=["File Name", "Number of Maskings", "Adhar Number" , "Number of Pages" , "Masking done on pages"])
# # #         writer.writeheader()
# # #         for data in summary_data:
# # #             # Use a set to ensure unique masked numbers
# # #             beforeunique_masked_numbers = data["masked_numbers"]
# # #             unique_masked_numbers = set(data["masked_numbers"])
# # #             # print(len(beforeunique_masked_numbers), "is the length")
# # #             writer.writerow({
# # #                 "File Name": data["file_name"],
# # #                 "Number of Maskings": len(beforeunique_masked_numbers),
# # #                 "Adhar Number": ", ".join(sorted(unique_masked_numbers)),
# # #                 "Number of Pages": data["number_of_pages"],
# # #                 "Masking done on pages": ", ".join(map(str, data["masking_done_on_pages"]))

# # #             })
# # #     return csv_filename


# # # # Routes
# # # @app.route('/')
# # # def home():
# # #     return redirect(url_for('login_user'))
# # # @app.route('/login', methods=['GET', 'POST'])
# # # def login_user():
# # #     if request.method == 'POST':
# # #         username = request.form.get('username')
# # #         password = request.form.get('password')

# # #         # Check credentials
# # #         if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
# # #             return redirect(url_for('index'))
# # #         else:
# # #             error = "Invalid username or password"
# # #             return render_template('login.html', error=error)

# # #     return render_template('login.html')
# # # @app.route('/index', methods=['GET'])
# # # def index():
# # #     return render_template('index.html')

# # # @app.route('/upload', methods=['POST'])
# # # def upload_file():
# # #     if 'files' not in request.files:
# # #         return "No files part", 400

# # #     files = request.files.getlist('files')
# # #     if len(files) == 0:
# # #         return "No files selected", 400

# # #     session_id = str(uuid.uuid4())  # Unique ID for this upload session
# # #     zip_filename = f"processed_files_{session_id}.zip"
# # #     zip_filepath = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)

# # #     summary_data = []  # Store details for the summary CSV

# # #     try:
# # #         with zipfile.ZipFile(zip_filepath, 'w') as zipf:
# # #             for file in files:
# # #                 filename = secure_filename(file.filename)
# # #                 input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # #                 file.save(input_pdf_path)

# # #                 # Process the file
# # #                 output_pdf_path = os.path.join(app.config['PROCESSED_FOLDER'], f"masked_{filename}")
# # #                 file_summary = mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id)

# # #                 if file_summary:
# # #                     summary_data.append(file_summary)

# # #                     # Add processed file to the ZIP archive
# # #                     zipf.write(output_pdf_path, arcname=os.path.basename(output_pdf_path))

# # #             # Generate and add the summary CSV to the ZIP archive
# # #             summary_csv_path = generate_summary_csv(summary_data, app.config['PROCESSED_FOLDER'], session_id)
# # #             zipf.write(summary_csv_path, arcname=os.path.basename(summary_csv_path))

# # #         # Provide a single ZIP download link
# # #         return redirect(url_for('download_file', filename=zip_filename))
# # #     finally:
# # #         # Cleanup if needed (optional)
# # #         active_uploads.pop(session_id, None)


# # # @app.route('/download/<filename>')
# # # def download_file(filename):
# # #     file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
# # #     return send_file(file_path, as_attachment=True)

# # # @app.route('/cancel', methods=['POST'])
# # # def cancel_upload():
# # #     # Handle cancel request
# # #     for session_files in active_uploads.values():
# # #         for file_path in session_files:
# # #             if os.path.exists(file_path):
# # #                 os.remove(file_path)
# # #     active_uploads.clear()
# # #     return jsonify({"message": "Uploads canceled successfully!"}), 200

# # # if __name__ == '__main__':
# # #     app.run(debug=True)
# # #     #ui.run()
# from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
# import os
# from werkzeug.utils import secure_filename
# import fitz
# from PIL import Image, ImageDraw
# import easyocr
# import re
# import cv2
# import numpy as np
# import uuid
# import zipfile
# import csv
# from concurrent.futures import ThreadPoolExecutor

# # Initialize Flask app
# app = Flask(__name__)

# # User credentials for login
# USER_CREDENTIALS = {
#     "admin": "pa",
#     "user": "userpass"
# }

# # Set upload and processed directories
# UPLOAD_FOLDER = "uploads"
# PROCESSED_FOLDER = "processed"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# # Helper functions
# def is_valid_12digit_number(text):
#     """Check if a given text contains a valid 12-digit number."""
#     processed_text = re.sub(r'\D', '', text)
#     return len(processed_text) == 12

# def expand_bbox(bbox, padding=5):
#     """Expand bounding box coordinates with padding."""
#     top_left = (int(bbox[0][0] - padding), int(bbox[0][1] - padding))
#     bottom_right = (int(bbox[2][0] + padding), int(bbox[2][1] + padding))
#     return top_left, bottom_right

# def mask_page(page, reader, session_id, page_num):
#     """Mask numbers on a single PDF page."""
#     pix = page.get_pixmap(dpi=150)  # Render page as an image
#     img_cv = np.frombuffer(pix.tobytes(), np.uint8)
#     img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

#     if img_cv is None:
#         raise ValueError(f"Error decoding image data for page {page_num + 1}")

#     # OCR processing
#     result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=5)

#     # Create an editable PIL image
#     img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
#     draw = ImageDraw.Draw(img_pil)

#     masked_numbers = []
#     for bbox, text, score in result:
#         if is_valid_12digit_number(text):
#             top_left, bottom_right = expand_bbox(bbox)
#             draw.rectangle([top_left, bottom_right], fill=(0, 0, 0))
#             masked_numbers.append(text)

#     # Return the masked image and masked numbers
#     return img_pil.convert("RGB"), masked_numbers

# def mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id):
#     """Mask 12-digit numbers in a PDF file."""
#     doc = fitz.open(input_pdf_path)
#     reader = easyocr.Reader(['en'], gpu=False)

#     masked_pages = []
#     all_masked_numbers = []
#     masking_count = 0
#     pages_masked = []

#     with ThreadPoolExecutor() as executor:
#         futures = []
#         for page_num in range(len(doc)):
#             page = doc.load_page(page_num)
#             futures.append(executor.submit(mask_page, page, reader, session_id, page_num))

#         for page_num, future in enumerate(futures):
#             img_pil, masked_numbers = future.result()
#             masked_pages.append(img_pil)
#             all_masked_numbers.extend(masked_numbers)
#             if masked_numbers:
#                 pages_masked.append(page_num + 1)
#                 masking_count += len(masked_numbers)

#     # Save the masked pages to a new PDF
#     doc.close()
#     doc = fitz.open()
#     for img in masked_pages:
#         temp_img_path = f"{uuid.uuid4().hex}.png"
#         img.save(temp_img_path, format="PNG")
#         imgdoc = fitz.open(temp_img_path)
#         pdfbytes = imgdoc.convert_to_pdf()
#         imgpdf = fitz.open("pdf", pdfbytes)
#         doc.insert_pdf(imgpdf)
#         os.remove(temp_img_path)

#     doc.save(output_pdf_path)
#     doc.close()

#     return {
#         "file_name": os.path.basename(output_pdf_path),
#         "masking_count": masking_count,
#         "masked_numbers": all_masked_numbers,
#         "number_of_pages": len(masked_pages),
#         "masking_done_on_pages": pages_masked
#     }

# def generate_summary_csv(summary_data, output_folder, session_id):
#     """Generate a summary CSV file."""
#     csv_filename = os.path.join(output_folder, f"Masking_Summary_{session_id}.csv")
#     with open(csv_filename, mode='w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=[
#             "File Name", "Number of Maskings", "Masked Numbers", "Number of Pages", "Masking Done on Pages"
#         ])
#         writer.writeheader()
#         for data in summary_data:
#             writer.writerow({
#                 "File Name": data["file_name"],
#                 "Number of Maskings": data["masking_count"],
#                 "Masked Numbers": ", ".join(set(data["masked_numbers"])),
#                 "Number of Pages": data["number_of_pages"],
#                 "Masking Done on Pages": ", ".join(map(str, data["masking_done_on_pages"]))
#             })
#     return csv_filename

# # Routes
# @app.route('/')
# def home():
#     return redirect(url_for('login_user'))

# @app.route('/login', methods=['GET', 'POST'])
# def login_user():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
#             return redirect(url_for('index'))
#         else:
#             error = "Invalid username or password"
#             return render_template('login.html', error=error)
#     return render_template('login.html')

# @app.route('/index', methods=['GET'])
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'files' not in request.files:
#         return "No files part", 400

#     files = request.files.getlist('files')
#     if len(files) == 0:
#         return "No files selected", 400

#     session_id = str(uuid.uuid4())
#     zip_filename = f"processed_files_{session_id}.zip"
#     zip_filepath = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)

#     summary_data = []

#     with zipfile.ZipFile(zip_filepath, 'w') as zipf:
#         for file in files:
#             filename = secure_filename(file.filename)
#             input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(input_pdf_path)

#             output_pdf_path = os.path.join(app.config['PROCESSED_FOLDER'], f"masked_{filename}")
#             file_summary = mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id)
#             summary_data.append(file_summary)

#             zipf.write(output_pdf_path, arcname=os.path.basename(output_pdf_path))

#         summary_csv_path = generate_summary_csv(summary_data, app.config['PROCESSED_FOLDER'], session_id)
#         zipf.write(summary_csv_path, arcname=os.path.basename(summary_csv_path))

#     return redirect(url_for('download_file', filename=zip_filename))

# @app.route('/download/<filename>')
# def download_file(filename):
#     file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
#     return send_file(file_path, as_attachment=True)

# # Main entry point
# if __name__ == '__main__':
#     app.run(debug=True)


# # from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
# # import os
# # from werkzeug.utils import secure_filename
# # import fitz
# # from PIL import Image, ImageDraw
# # import easyocr
# # import re
# # import cv2
# # import numpy as np
# # import uuid
# # import zipfile
# # import csv
# # import sys
# # import tempfile
# # from concurrent.futures import ThreadPoolExecutor

# # # Initialize Flask app
# # app = Flask(__name__)

# # # User credentials for login
# # USER_CREDENTIALS = {
# #     "admin": "password123",
# #     "user": "userpass"
# # }

# # # Helper function to handle dynamic paths for bundled resources
# # def get_resource_path(relative_path):
# #     """Get the resource path in frozen mode (PyInstaller)."""
# #     if getattr(sys, 'frozen', False):
# #         # In frozen mode, use _MEIPASS for accessing bundled files
# #         return os.path.join(sys._MEIPASS, relative_path)
# #     else:
# #         # In development mode, just return the relative path
# #         return os.path.join(os.path.dirname(__file__), relative_path)

# # # Set upload and processed directories
# # UPLOAD_FOLDER = get_resource_path("uploads")
# # PROCESSED_FOLDER = get_resource_path("processed")
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# # # Helper functions
# # def is_valid_12digit_number(text):
# #     """Check if a given text contains a valid 12-digit number."""
# #     processed_text = re.sub(r'\D', '', text)
# #     return len(processed_text) == 12

# # def expand_bbox(bbox, padding=5):
# #     """Expand bounding box coordinates with padding."""
# #     top_left = (int(bbox[0][0] - padding), int(bbox[0][1] - padding))
# #     bottom_right = (int(bbox[2][0] + padding), int(bbox[2][1] + padding))
# #     return top_left, bottom_right

# # def mask_page(page, reader, session_id, page_num):
# #     """Mask numbers on a single PDF page."""
# #     pix = page.get_pixmap(dpi=150)  # Render page as an image
# #     img_cv = np.frombuffer(pix.tobytes(), np.uint8)
# #     img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

# #     if img_cv is None:
# #         raise ValueError(f"Error decoding image data for page {page_num + 1}")

# #     # OCR processing
# #     result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=5)

# #     # Create an editable PIL image
# #     img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
# #     draw = ImageDraw.Draw(img_pil)

# #     masked_numbers = []
# #     for bbox, text, score in result:
# #         if is_valid_12digit_number(text):
# #             top_left, bottom_right = expand_bbox(bbox)
# #             draw.rectangle([top_left, bottom_right], fill=(0, 0, 0))
# #             masked_numbers.append(text)

# #     # Return the masked image and masked numbers
# #     return img_pil.convert("RGB"), masked_numbers

# # def mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id):
# #     """Mask 12-digit numbers in a PDF file."""
# #     doc = fitz.open(input_pdf_path)
# #     reader = easyocr.Reader(['en'], gpu=True)

# #     masked_pages = []
# #     all_masked_numbers = []
# #     masking_count = 0
# #     pages_masked = []

# #     with ThreadPoolExecutor() as executor:
# #         futures = []
# #         for page_num in range(len(doc)):
# #             page = doc.load_page(page_num)
# #             futures.append(executor.submit(mask_page, page, reader, session_id, page_num))

# #         for page_num, future in enumerate(futures):
# #             img_pil, masked_numbers = future.result()
# #             masked_pages.append(img_pil)
# #             all_masked_numbers.extend(masked_numbers)
# #             if masked_numbers:
# #                 pages_masked.append(page_num + 1)
# #                 masking_count += len(masked_numbers)

# #     # Save the masked pages to a new PDF
# #     doc.close()
# #     doc = fitz.open()
# #     for img in masked_pages:
# #         temp_img_path = f"{uuid.uuid4().hex}.png"
# #         img.save(temp_img_path, format="PNG")
# #         imgdoc = fitz.open(temp_img_path)
# #         pdfbytes = imgdoc.convert_to_pdf()
# #         imgpdf = fitz.open("pdf", pdfbytes)
# #         doc.insert_pdf(imgpdf)
# #         os.remove(temp_img_path)

# #     doc.save(output_pdf_path)
# #     doc.close()

# #     return {
# #         "file_name": os.path.basename(output_pdf_path),
# #         "masking_count": masking_count,
# #         "masked_numbers": all_masked_numbers,
# #         "number_of_pages": len(masked_pages),
# #         "masking_done_on_pages": pages_masked
# #     }

# # def generate_summary_csv(summary_data, output_folder, session_id):
# #     """Generate a summary CSV file."""
# #     csv_filename = os.path.join(output_folder, f"Masking_Summary_{session_id}.csv")
# #     with open(csv_filename, mode='w', newline='') as csvfile:
# #         writer = csv.DictWriter(csvfile, fieldnames=[
# #             "File Name", "Number of Maskings", "Masked Numbers", "Number of Pages", "Masking Done on Pages"
# #         ])
# #         writer.writeheader()
# #         for data in summary_data:
# #             writer.writerow({
# #                 "File Name": data["file_name"],
# #                 "Number of Maskings": data["masking_count"],
# #                 "Masked Numbers": ", ".join(set(data["masked_numbers"])),
# #                 "Number of Pages": data["number_of_pages"],
# #                 "Masking Done on Pages": ", ".join(map(str, data["masking_done_on_pages"]))
# #             })
# #     return csv_filename

# # # Routes
# # @app.route('/')
# # def home():
# #     return redirect(url_for('login_user'))

# # @app.route('/login', methods=['GET', 'POST'])
# # def login_user():
# #     if request.method == 'POST':
# #         username = request.form.get('username')
# #         password = request.form.get('password')

# #         if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
# #             return redirect(url_for('index'))
# #         else:
# #             error = "Invalid username or password"
# #             return render_template('login.html', error=error)
# #     return render_template('login.html')

# # @app.route('/index', methods=['GET'])
# # def index():
# #     return render_template('index.html')

# # @app.route('/upload', methods=['POST'])
# # def upload_file():
# #     if 'files' not in request.files:
# #         return "No files part", 400

# #     files = request.files.getlist('files')
# #     if len(files) == 0:
# #         return "No files selected", 400

# #     session_id = str(uuid.uuid4())
# #     zip_filename = f"processed_files_{session_id}.zip"
# #     zip_filepath = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)

# #     summary_data = []

# #     with zipfile.ZipFile(zip_filepath, 'w') as zipf:
# #         for file in files:
# #             filename = secure_filename(file.filename)
# #             input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #             file.save(input_pdf_path)

# #             output_pdf_path = os.path.join(app.config['PROCESSED_FOLDER'], f"masked_{filename}")
# #             file_summary = mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id)
# #             summary_data.append(file_summary)

# #             zipf.write(output_pdf_path, arcname=os.path.basename(output_pdf_path))

# #         summary_csv_path = generate_summary_csv(summary_data, app.config['PROCESSED_FOLDER'], session_id)
# #         zipf.write(summary_csv_path, arcname=os.path.basename(summary_csv_path))

# #     return redirect(url_for('download_file', filename=zip_filename))

# # @app.route('/download/<filename>')
# # def download_file(filename):
# #     file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
# #     return send_file(file_path, as_attachment=True)

# # # Main entry point
# # if __name__ == '__main__':
# #     app.run(debug=True)

# # #last version 
# # #-----------------------------------------------------------
# # from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
# # import os
# # from werkzeug.utils import secure_filename
# # import fitz
# # from PIL import Image, ImageDraw
# # import easyocr
# # import re
# # import cv2
# # import numpy as np
# # import uuid
# # import zipfile
# # import csv
# # import sys
# # from concurrent.futures import ThreadPoolExecutor

# # # Initialize Flask app
# # app = Flask(__name__)

# # # User credentials for login
# # USER_CREDENTIALS = {
# #     "admin": "password123",
# #     "user": "userpass"
# # }

# # # Helper function to handle dynamic paths for bundled resources
# # def get_resource_path(relative_path):
# #     """Get the resource path in frozen mode (PyInstaller)."""
# #     if getattr(sys, 'frozen', False):
# #         return os.path.join(sys._MEIPASS, relative_path)
# #     else:
# #         return os.path.join(os.path.dirname(__file__), relative_path)

# # # Set upload and processed directories
# # UPLOAD_FOLDER = get_resource_path("uploads")
# # PROCESSED_FOLDER = get_resource_path("processed")
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# # # Initialize EasyOCR Reader globally
# # reader = easyocr.Reader(['en'], gpu=False, detector='dbnet18')

# # # Helper functions
# # def is_valid_12digit_number(text):
# #     """Check if a given text contains a valid 12-digit number."""
# #     processed_text = re.sub(r'\D', '', text)
# #     return len(processed_text) == 12

# # def expand_bbox(bbox, padding=5):
# #     """Expand bounding box coordinates with padding."""
# #     top_left = (int(bbox[0][0] - padding), int(bbox[0][1] - padding))
# #     bottom_right = (int(bbox[2][0] + padding), int(bbox[2][1] + padding))
# #     return top_left, bottom_right

# # def mask_page(page, session_id, page_num):
# #     """Mask numbers on a single PDF page."""
# #     pix = page.get_pixmap(dpi=150)
# #     img_cv = np.frombuffer(pix.tobytes(), np.uint8)
# #     img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

# #     if img_cv is None:
# #         raise ValueError(f"Error decoding image data for page {page_num + 1}")

# #     # OCR processing
# #     result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=10)

# #     # Create an editable PIL image
# #     img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
# #     draw = ImageDraw.Draw(img_pil)

# #     masked_numbers = []
# #     for bbox, text, score in result:
# #         if is_valid_12digit_number(text):
# #             top_left, bottom_right = expand_bbox(bbox)
# #             draw.rectangle([top_left, bottom_right], fill=(0, 0, 0))
# #             masked_numbers.append(text)

# #     return img_pil.convert("RGB"), masked_numbers

# # def mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id):
# #     """Mask 12-digit numbers in a PDF file."""
# #     doc = fitz.open(input_pdf_path)

# #     masked_pages = []
# #     all_masked_numbers = []
# #     masking_count = 0
# #     pages_masked = []

# #     with ThreadPoolExecutor() as executor:
# #         futures = []
# #         for page_num in range(len(doc)):
# #             page = doc.load_page(page_num)
# #             futures.append(executor.submit(mask_page, page, session_id, page_num))

# #         for page_num, future in enumerate(futures):
# #             img_pil, masked_numbers = future.result()
# #             masked_pages.append(img_pil)
# #             all_masked_numbers.extend(masked_numbers)
# #             if masked_numbers:
# #                 pages_masked.append(page_num + 1)
# #                 masking_count += len(masked_numbers)

# #     doc.close()
# #     doc = fitz.open()
# #     for img in masked_pages:
# #         temp_img_path = f"{uuid.uuid4().hex}.png"
# #         img.save(temp_img_path, format="PNG")
# #         imgdoc = fitz.open(temp_img_path)
# #         pdfbytes = imgdoc.convert_to_pdf()
# #         imgpdf = fitz.open("pdf", pdfbytes)
# #         doc.insert_pdf(imgpdf)
# #         os.remove(temp_img_path)

# #     doc.save(output_pdf_path)
# #     doc.close()

# #     return {
# #         "file_name": os.path.basename(output_pdf_path),
# #         "masking_count": masking_count,
# #         "masked_numbers": all_masked_numbers,
# #         "number_of_pages": len(masked_pages),
# #         "masking_done_on_pages": pages_masked
# #     }

# # def generate_summary_csv(summary_data, output_folder, session_id):
# #     """Generate a summary CSV file."""
# #     csv_filename = os.path.join(output_folder, f"Masking_Summary_{session_id}.csv")
# #     with open(csv_filename, mode='w', newline='') as csvfile:
# #         writer = csv.DictWriter(csvfile, fieldnames=[
# #             "File Name", "Number of Maskings", "Masked Numbers", "Number of Pages", "Masking Done on Pages"
# #         ])
# #         writer.writeheader()
# #         for data in summary_data:
# #             writer.writerow({
# #                 "File Name": data["file_name"],
# #                 "Number of Maskings": data["masking_count"],
# #                 "Masked Numbers": ", ".join(set(data["masked_numbers"])),
# #                 "Number of Pages": data["number_of_pages"],
# #                 "Masking Done on Pages": ", ".join(map(str, data["masking_done_on_pages"]))
# #             })
# #     return csv_filename

# # # Routes
# # @app.route('/')
# # def home():
# #     return redirect(url_for('login_user'))

# # @app.route('/login', methods=['GET', 'POST'])
# # def login_user():
# #     if request.method == 'POST':
# #         username = request.form.get('username')
# #         password = request.form.get('password')

# #         if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
# #             return redirect(url_for('index'))
# #         else:
# #             error = "Invalid username or password"
# #             return render_template('login.html', error=error)
# #     return render_template('login.html')

# # @app.route('/index', methods=['GET'])
# # def index():
# #     return render_template('index.html')

# # @app.route('/upload', methods=['POST'])
# # def upload_file():
# #     try:
# #         if 'files' not in request.files:
# #             return jsonify({"error": "No files part"}), 400

# #         files = request.files.getlist('files')
# #         if len(files) == 0:
# #             return jsonify({"error": "No files selected"}), 400

# #         session_id = str(uuid.uuid4())
# #         zip_filename = f"processed_files_{session_id}.zip"
# #         zip_filepath = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)

# #         summary_data = []

# #         with zipfile.ZipFile(zip_filepath, 'w') as zipf:
# #             for file in files:
# #                 filename = secure_filename(file.filename)
# #                 input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #                 file.save(input_pdf_path)

# #                 output_pdf_path = os.path.join(app.config['PROCESSED_FOLDER'], f"masked_{filename}")
# #                 file_summary = mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id)
# #                 summary_data.append(file_summary)

# #                 zipf.write(output_pdf_path, arcname=os.path.basename(output_pdf_path))

# #             summary_csv_path = generate_summary_csv(summary_data, app.config['PROCESSED_FOLDER'], session_id)
# #             zipf.write(summary_csv_path, arcname=os.path.basename(summary_csv_path))

# #         return jsonify({"success": True, "filename": zip_filename}), 200

# #     except Exception as e:
# #         # Log exception and return error
# #         print(f"Error during upload processing: {e}")
# #         return jsonify({"error": str(e)}), 500

# # # @app.route('/download/<filename>')
# # # def download_file(filename):
# # #     file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
# # #     return send_file(file_path, as_attachment=True)

# # @app.route('/download/<filename>')
# # def download_file(filename):
# #     try:
# #         file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
# #         if not os.path.exists(file_path):
# #             return jsonify({"error": "File not found"}), 404
# #         return send_file(file_path, as_attachment=True)
# #     except Exception as e:
# #         print(f"Error during file download: {e}")
# #         return jsonify({"error": str(e)}), 500


# # # Main entry point
# # if __name__ == '__main__':
# #     app.run(debug=True)




#nigagaggagagga
#-----------------------------------------------------------
#-----------------------------------------------------------

# from flask import Flask, request, render_template, send_file, redirect, url_for , jsonify
# import os
# from werkzeug.utils import secure_filename
# import pdf2image
# import fitz
# from PIL import Image, ImageDraw
# import easyocr
# import re
# import cv2
# import numpy as np
# import uuid
# import zipfile
# import csv 

# # Initialize Flask app
# app = Flask(__name__)
# USER_CREDENTIALS = {
#     "admin": "password123",  # Replace with your desired username and password
#     "user": "userpass"
# }
# # from flaskwebgui import FlaskUI
# # ui = FlaskUI(app)
# # Set upload and output directories

# # Helper function to handle dynamic paths for bundled resources
# def get_resource_path(relative_path):
#     """Get the resource path in frozen mode (PyInstaller)."""
#     if getattr(sys, 'frozen', False):
#         return os.path.join(sys._MEIPASS, relative_path)
#     else:
#         return os.path.join(os.path.dirname(__file__), relative_path)
# UPLOAD_FOLDER = "uploads"
# PROCESSED_FOLDER = "processed"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(PROCESSED_FOLDER, exist_ok=True)  

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
# reader = easyocr.Reader(['en'], gpu=False)
# active_uploads = {}

# # Helper functions
# def is_valid_12digit_number(text):
#     """Check if a given text contains a valid 12-digit number."""
#     processed_text = re.sub(r'\D', '', text)
#     return len(processed_text) == 12

# def expand_bbox(bbox, padding=5):
#     top_left = (int(bbox[0][0] - padding), int(bbox[0][1] - padding))
#     bottom_right = (int(bbox[2][0] + padding), int(bbox[2][1] + padding))
#     return top_left, bottom_right



# def mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id):
#     doc = fitz.open(input_pdf_path)  # Open PDF document
#     masked_pages = []
#     masked_numbers = []  # Collect all masked 12-digit numbers
#     masking_count = 0    # Count of maskings done
#     count = 0

#     pagestobefoundon = []

#     for page_num in range(len(doc)):
#         count += 1
#         page = doc.load_page(page_num)  # Load a single page
#         pix = page.get_pixmap(dpi=300)  # Render page as an image

#         # Convert pixmap to OpenCV format
#         img_cv = np.frombuffer(pix.tobytes(), np.uint8)
#         img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

#         if img_cv is None:
#             raise ValueError(f"Error decoding image data for page {count}")
        
#         result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=5)

        

#         # Create an editable PIL image
#         img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
#         draw = ImageDraw.Draw(img_pil)

#         for bbox, text, score in result:
            

#             if is_valid_12digit_number(text):
#                 pagestobefoundon.append(count)
#                 top_left, bottom_right = expand_bbox(bbox)
#                 bbox_width = bottom_right[0] - top_left[0]
#                 adjusted_width = bbox_width * (8 / 12)
#                 adjusted_bottom_right = (top_left[0] + adjusted_width, bottom_right[1])
                
#                 draw.rectangle([top_left, adjusted_bottom_right], fill=(0, 0, 0))

#                 masked_numbers.append(text)
#                 masking_count += 1

#         # Save the modified image to the masked_pages list
#         img_pil = img_pil.convert("RGB")
#         masked_pages.append(img_pil)

#     # Save the masked pages back to a PDF
#     doc.close()
#     doc = fitz.open()  # Create a new PDF
#     for img in masked_pages:
#         # Save each page as a temporary image file
#         temp_img_path = f"{uuid.uuid4().hex}.png"
#         img.save(temp_img_path, format="PNG")

#         # Load the temporary image into a PDF page
#         imgdoc = fitz.open(temp_img_path)
#         pdfbytes = imgdoc.convert_to_pdf()
#         imgpdf = fitz.open("pdf", pdfbytes)
#         doc.insert_pdf(imgpdf)

#         # Clean up the temporary image
#         os.remove(temp_img_path)

#     doc.save(output_pdf_path)
#     doc.close()

#     return {
#         "file_name": os.path.basename(output_pdf_path),
#         "masking_count": masking_count,
#         "masked_numbers": masked_numbers,
#         "number_of_pages": len(masked_pages),
#         "masking_done_on_pages": pagestobefoundon
#     }



# def generate_summary_csv(summary_data, output_folder, session_id):
#     csv_filename = os.path.join(output_folder, f"Adhar Masking Summary.csv")
#     with open(csv_filename, mode='w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=["File Name", "Number of Maskings", "Adhar Number" , "Number of Pages" , "Masking done on pages"])
#         writer.writeheader()
#         for data in summary_data:
#             # Use a set to ensure unique masked numbers
#             beforeunique_masked_numbers = data["masked_numbers"]
#             unique_masked_numbers = set(data["masked_numbers"])
#             # print(len(beforeunique_masked_numbers), "is the length")
#             writer.writerow({
#                 "File Name": data["file_name"],
#                 "Number of Maskings": len(beforeunique_masked_numbers),
#                 "Adhar Number": ", ".join(sorted(unique_masked_numbers)),
#                 "Number of Pages": data["number_of_pages"],
#                 "Masking done on pages": ", ".join(map(str, data["masking_done_on_pages"]))

#             })
#     return csv_filename


# # Routes
# @app.route('/')
# def home():
#     return redirect(url_for('login_user'))
# @app.route('/login', methods=['GET', 'POST'])
# def login_user():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         # Check credentials
#         if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
#             return redirect(url_for('index'))
#         else:
#             error = "Invalid username or password"
#             return render_template('login.html', error=error)

#     return render_template('login.html')
# @app.route('/index', methods=['GET'])
# def index():
#     return render_template('index.html')
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'files' not in request.files:
#         return jsonify({"error": "No files part"}), 400

#     files = request.files.getlist('files')
#     if len(files) == 0:
#         return jsonify({"error": "No files selected"}), 400

#     try:
#         session_id = str(uuid.uuid4())
#         zip_filename = f"processed_files_{session_id}.zip"
#         zip_filepath = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)

#         summary_data = []

#         with zipfile.ZipFile(zip_filepath, 'w') as zipf:
#             for file in files:
#                 filename = secure_filename(file.filename)
#                 input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(input_pdf_path)

#                 output_pdf_path = os.path.join(app.config['PROCESSED_FOLDER'], f"masked_{filename}")
#                 file_summary = mask_numbers_in_pdf(input_pdf_path, output_pdf_path, session_id)
#                 summary_data.append(file_summary)

#                 zipf.write(output_pdf_path, arcname=os.path.basename(output_pdf_path))

#             summary_csv_path = generate_summary_csv(summary_data, app.config['PROCESSED_FOLDER'], session_id)
#             zipf.write(summary_csv_path, arcname=os.path.basename(summary_csv_path))

#         return jsonify({
#             "success": True,
#             "filename": zip_filename
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/download/<filename>')
# def download_file(filename):
#     try:
#         file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
#         return send_file(file_path, as_attachment=True, download_name=filename)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 404

# @app.route('/cancel', methods=['POST'])
# def cancel_upload():
#     # Handle cancel request
#     for session_files in active_uploads.values():
#         for file_path in session_files:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#     active_uploads.clear()
#     return jsonify({"message": "Uploads canceled successfully!"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)
#     #ui.run()











from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import os
from io import StringIO
from werkzeug.utils import secure_filename
import fitz
from PIL import Image, ImageDraw
import easyocr
import re
import cv2
import numpy as np
import uuid
import zipfile
import sys
import csv
import logging
from multiprocessing import Pool
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)

# User credentials for login
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "userpass"
}

# Helper function to handle dynamic paths for bundled resources
def get_resource_path(relative_path):
    """Get the resource path in frozen mode (PyInstaller)."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.dirname(__file__), relative_path)

# Set upload and processed directories
UPLOAD_FOLDER = get_resource_path("uploads")
PROCESSED_FOLDER = get_resource_path("processed")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Initialize EasyOCR Reader globally
reader = easyocr.Reader(['en'], gpu=False)

# Helper functions
def is_valid_12digit_number(text):
    """
    Check if a given text contains exactly 12 digits,
    optionally separated by spaces, and nothing else.
    """
    # Match a pattern of exactly 12 digits with optional spaces between them
    pattern = r'^(\d\s*){12}$'
    return bool(re.match(pattern, text.strip()))

def expand_bbox(bbox, padding=5):
    """Expand bounding box coordinates with padding."""
    top_left = (int(bbox[0][0] - padding), int(bbox[0][1] - padding))
    bottom_right = (int(bbox[2][0] + padding), int(bbox[2][1] + padding))
    return top_left, bottom_right

def process_page(args):
    """Process a single page to mask numbers."""
    pdf_path, page_num, session_id = args
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=150)  # Lower DPI for faster processing
    img_cv = np.frombuffer(pix.tobytes(), np.uint8)
    img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

    if img_cv is None:
        raise ValueError(f"Error decoding image data for page {page_num + 1}")

    # OCR processing
    result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=10)

    # Create an editable PIL image
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    masked_numbers = []
    for bbox, text, score in result:
        print(text)
        if is_valid_12digit_number(text):
            top_left, bottom_right = expand_bbox(bbox)
            draw.rectangle([top_left, bottom_right], fill=(0, 0, 0))
            masked_numbers.append(text)

    doc.close()
    return img_pil.convert("RGB"), masked_numbers



# def process_pdf(input_pdf_path, session_id):
#     """Process a PDF to mask 12-digit numbers with compression."""
#     doc = fitz.open(input_pdf_path)
#     total_pages = len(doc)
#     reader = easyocr.Reader(['en'], gpu=True)
#     masked_pages = []
#     all_masked_numbers = []
#     masking_count = 0
#     pages_masked = []

#     for page_num in range(total_pages):
#         logging.info(f"Processing page {page_num + 1}/{total_pages}")
#         page = doc.load_page(page_num)
#         pix = page.get_pixmap(dpi=150)  # Reduced DPI
#         img_cv = np.frombuffer(pix.tobytes(), np.uint8)
#         img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

#         if img_cv is None:
#             logging.warning(f"Failed to process page {page_num + 1}")
#             continue

        
        
#         result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=10)
#         img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
#         draw = ImageDraw.Draw(img_pil)

#         masked_numbers = []
#         for bbox, text, score in result:
#             if is_valid_12digit_number(text):
#                 top_left, bottom_right = expand_bbox(bbox)
#                 bbox_width = bottom_right[0] - top_left[0]
#                 adjusted_width = bbox_width * (8 / 12)
#                 adjusted_bottom_right = (top_left[0] + adjusted_width, bottom_right[1])
#                 draw.rectangle([top_left, adjusted_bottom_right], fill=(0, 0, 0))
#                 masked_numbers.append(text)

#         # Compress image after masking
#         img_buffer = BytesIO()
#         img_pil.save(img_buffer, format="JPEG", quality=65, optimize=True)  # Use JPEG with compression
#         img_pil = Image.open(img_buffer)
        
#         masked_pages.append(img_pil)
#         all_masked_numbers.extend(masked_numbers)
#         if masked_numbers:
#             pages_masked.append(page_num + 1)
#             masking_count += len(masked_numbers)

#     output = BytesIO()
#     doc = fitz.open()
#     for img in masked_pages:
#         img_buffer = BytesIO()
#         img.save(img_buffer, format="JPEG", quality=85, optimize=True)
#         imgdoc = fitz.open(stream=img_buffer.getvalue(), filetype="jpeg")
#         pdfbytes = imgdoc.convert_to_pdf()
#         imgpdf = fitz.open("pdf", pdfbytes)
#         doc.insert_pdf(imgpdf)
    
#     # Set PDF compression
#     doc.save(output, deflate=True, garbage=4, clean=True)
#     doc.close()

#     return {
#         "file_content": output.getvalue(),
#         "masking_count": masking_count,
#         "masked_numbers": all_masked_numbers,
#         "number_of_pages": total_pages,
#         "masking_done_on_pages": pages_masked
#     }

def process_pdf(input_pdf, session_id):
    """Process a PDF from BytesIO to mask 12-digit numbers with compression."""
    doc = fitz.open(stream=input_pdf.read(), filetype="pdf")
    total_pages = len(doc)
    reader = easyocr.Reader(['en'], gpu=True)
    masked_pages = []
    all_masked_numbers = []
    masking_count = 0
    pages_masked = []

    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img_cv = np.frombuffer(pix.tobytes(), np.uint8)
        img_cv = cv2.imdecode(img_cv, cv2.IMREAD_COLOR)

        if img_cv is None:
            continue

        result = reader.readtext(img_cv, detail=1, low_text=0.3, batch_size=10)
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        masked_numbers = []
        for bbox, text, score in result:
            if is_valid_12digit_number(text):
                top_left, bottom_right = expand_bbox(bbox)
                bbox_width = bottom_right[0] - top_left[0]
                adjusted_width = bbox_width * (8 / 12)
                adjusted_bottom_right = (top_left[0] + adjusted_width, bottom_right[1])
                draw.rectangle([top_left, adjusted_bottom_right], fill=(0, 0, 0))
                masked_numbers.append(text)

        img_buffer = BytesIO()
        img_pil.save(img_buffer, format="JPEG", quality=65, optimize=True)
        img_pil = Image.open(img_buffer)
        
        masked_pages.append(img_pil)
        all_masked_numbers.extend(masked_numbers)
        if masked_numbers:
            pages_masked.append(page_num + 1)
            masking_count += len(masked_numbers)

    output = BytesIO()
    pdf_doc = fitz.open()
    for img in masked_pages:
        img_buffer = BytesIO()
        img.save(img_buffer, format="JPEG", quality=85, optimize=True)
        imgdoc = fitz.open(stream=img_buffer.getvalue(), filetype="jpeg")
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        pdf_doc.insert_pdf(imgpdf)
    
    pdf_doc.save(output, deflate=True, garbage=4, clean=True)
    pdf_doc.close()
    doc.close()

    return {
        "file_content": output.getvalue(),
        "masking_count": masking_count,
        "masked_numbers": all_masked_numbers,
        "number_of_pages": total_pages,
        "masking_done_on_pages": pages_masked
    }
def generate_summary_csv(summary_data, output_folder, session_id):
    """Generate a summary CSV file."""
    csv_filename = os.path.join(output_folder, f"Masking_Summary_{session_id}.csv")
    with open(csv_filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "File Name", "Number of Maskings", "Masked Numbers", "Number of Pages", "Masking Done on Pages"
        ])
        writer.writeheader()
        for data in summary_data:
            writer.writerow({
                "File Name": data["file_name"],
                "Number of Maskings": data["masking_count"],
                "Masked Numbers": ", ".join(set(data["masked_numbers"])),
                "Number of Pages": data["number_of_pages"],
                "Masking Done on Pages": ", ".join(map(str, data["masking_done_on_pages"]))
            })
    return csv_filename

# Routes
@app.route('/')
def home():
    return redirect(url_for('login_user'))

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files part"}), 400

        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "No files selected"}), 400

        session_id = str(uuid.uuid4())
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            summary_data = []
            for file in files:
                filename = secure_filename(file.filename)
                pdf_data = BytesIO(file.read())
                
                output = process_pdf(pdf_data, session_id)
                summary_data.append({
                    "file_name": filename,
                    **output
                })

                zipf.writestr(f"masked_{filename}", output["file_content"])

            # Create CSV in memory
            csv_buffer = StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=[
                "File Name", "Number of Maskings", "Masked Numbers", 
                "Number of Pages", "Masking Done on Pages"
            ])
            writer.writeheader()
            for data in summary_data:
                writer.writerow({
                    "File Name": data["file_name"],
                    "Number of Maskings": data["masking_count"],
                    "Masked Numbers": ", ".join(str(x) for x in data["masked_numbers"]),
                    "Number of Pages": data["number_of_pages"],
                    "Masking Done on Pages": ", ".join(map(str, data["masking_done_on_pages"]))
                })
            
            # Convert StringIO to bytes before adding to ZIP
            csv_content = csv_buffer.getvalue().encode('utf-8')
            zipf.writestr(f"Masking_Summary_{session_id}.csv", csv_content)

        zip_buffer.seek(0)
        app.config[f'zip_file_{session_id}'] = zip_buffer.getvalue()
        
        return jsonify({
            "success": True, 
            "filename": f"processed_files_{session_id}.zip"
        }), 200

    except Exception as e:
        print(f"Error during upload processing: {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/download/<filename>')
def download_file(filename):
    try:
        session_id = filename.split('_')[-1].split('.')[0]
        zip_data = app.config.get(f'zip_file_{session_id}')
        
        if not zip_data:
            return jsonify({"error": "File not found"}), 404
            
        return send_file(
            BytesIO(zip_data),
            mimetype='application/zip',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print(f"Error during file download: {e}")
        return jsonify({"error": str(e)}), 500
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         if 'files' not in request.files:
#             return jsonify({"error": "No files part"}), 400

#         files = request.files.getlist('files')
#         if len(files) == 0:
#             return jsonify({"error": "No files selected"}), 400

#         session_id = str(uuid.uuid4())
#         zip_filename = f"processed_files_{session_id}.zip"
#         zip_filepath = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)

#         summary_data = []

#         with zipfile.ZipFile(zip_filepath, 'w') as zipf:
#             for file in files:
#                 filename = secure_filename(file.filename)
#                 input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(input_pdf_path)

#                 output = process_pdf(input_pdf_path, session_id)
#                 summary_data.append({
#                     "file_name": filename,
#                     **output
#                 })

#                 zipf.writestr(f"masked_{filename}", output["file_content"])

#             summary_csv_path = generate_summary_csv(summary_data, app.config['PROCESSED_FOLDER'], session_id)
#             zipf.write(summary_csv_path, arcname=os.path.basename(summary_csv_path))

#         return jsonify({"success": True, "filename": zip_filename}), 200

#     except Exception as e:
#         print(f"Error during upload processing: {e}")
#         return jsonify({"error": str(e)}), 500

# @app.route('/download/<filename>')
# def download_file(filename):
#     try:
#         file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
#         if not os.path.exists(file_path):
#             return jsonify({"error": "File not found"}), 404
#         return send_file(file_path, as_attachment=True)
#     except Exception as e:
#         print(f"Error during file download: {e}")
#         return jsonify({"error": str(e)}), 500

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         if 'files' not in request.files:
#             return jsonify({"error": "No files part"}), 400

#         files = request.files.getlist('files')
#         if len(files) == 0:
#             return jsonify({"error": "No files selected"}), 400

#         session_id = str(uuid.uuid4())
#         zip_filename = f"processed_files_{session_id}.zip"
#         zip_filepath = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)

#         summary_data = []

#         with zipfile.ZipFile(zip_filepath, 'w') as zipf:
#             for file in files:
#                 filename = secure_filename(file.filename)
#                 input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(input_pdf_path)

#                 output = process_pdf(input_pdf_path, session_id)
#                 summary_data.append({
#                     "file_name": filename,
#                     **output
#                 })

#                 zipf.writestr(f"masked_{filename}", output["file_content"])

#             summary_csv_path = generate_summary_csv(summary_data, app.config['PROCESSED_FOLDER'], session_id)
#             zipf.write(summary_csv_path, arcname=os.path.basename(summary_csv_path))

#         return jsonify({"success": True, "filename": zip_filename}), 200

#     except Exception as e:
#         print(f"Error during upload processing: {e}")
#         return jsonify({"error": str(e)}), 500

# @app.route('/download/<filename>')
# def download_file(filename):
#     try:
#         file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
#         if not os.path.exists(file_path):
#             return jsonify({"error": "File not found"}), 404
#         return send_file(file_path, as_attachment=True)
#     except Exception as e:
#         print(f"Error during file download: {e}")
#         return jsonify({"error": str(e)}), 500
    
# @app.route('/cancel', methods=['POST'])
# def cancel_process():
#     # Logic to handle cancellation can go here
#     # For now, just return a success response
#     return jsonify({"message": "Process canceled successfully"}), 200
    
# def generate_summary_csv(summary_data, output_folder, session_id):
#     """Generate a summary CSV file."""
#     csv_filename = os.path.join(output_folder, f"Masking_Summary_{session_id}.csv")
#     with open(csv_filename, mode='w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=[
#             "File Name", "Number of Maskings", "Masked Numbers", "Number of Pages", "Masking Done on Pages"
#         ])
#         writer.writeheader()
#         for data in summary_data:
#             writer.writerow({
#                 "File Name": data["file_name"],
#                 "Number of Maskings": data["masking_count"],
#                 "Masked Numbers": ", ".join(set(data["masked_numbers"])),
#                 "Number of Pages": data["number_of_pages"],
#                 "Masking Done on Pages": ", ".join(map(str, data["masking_done_on_pages"]))
#             })
#     return csv_filename