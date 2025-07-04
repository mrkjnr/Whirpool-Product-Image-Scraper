from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os
import scrape_whirlpool_csv         # Custom module to scrape images based on CSV input
import zipfile                      # Used for creating a ZIP archive
import io                           # Used for in-memory file handling
from datetime import timedelta      # To set session expiration time

# Define where uploaded files will be stored temporarily
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}       # Only CSV uploads are allowed

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use session (store session variables)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.permanent_session_lifetime = timedelta(minutes=30)  # Session lifetime of 30 minutes

# Ensure the upload and image directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/whirlpool_images', exist_ok=True)

# Helper function to validate uploaded file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def index():
    # On first visit, clear old session and files
    if 'visited' not in session:
        session['visited'] = True

        # Delete existing images from previous sessions
        image_dir = os.path.join('static', 'whirlpool_images')
        for img_file in os.listdir(image_dir):
            img_path = os.path.join(image_dir, img_file)
            if os.path.isfile(img_path):
                os.remove(img_path)

        # Delete any previously uploaded CSV files
        for uploaded_file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Load all current images to display in gallery
    image_dir = os.path.join('static', 'whirlpool_images')
    images = os.listdir(image_dir) if os.path.exists(image_dir) else []
    return render_template('index.html', images=images)

# Route to handle CSV upload and trigger scraping
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Save uploaded CSV to uploads folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'whirlpool_parts.csv')
        file.save(filepath)

        # Remove any old images before new scraping run
        image_dir = os.path.join('static', 'whirlpool_images')
        for img_file in os.listdir(image_dir):
            img_path = os.path.join(image_dir, img_file)
            if os.path.isfile(img_path):
                os.remove(img_path)

        # Start image scraping using the uploaded CSV
        scrape_whirlpool_csv.scrape_images_from_csv(filepath)

        # Redirect back to homepage to display images
        return redirect(url_for('index'))

    # If uploaded file is not valid
    return "Invalid file format. Please upload a .csv file."

# Route to download all images as a ZIP file
@app.route('/download_images')
def download_images():
    image_dir = os.path.join('static', 'whirlpool_images')
    zip_buffer = io.BytesIO()  # Create an in-memory buffer for the ZIP

    # Write all images to ZIP file in memory
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(image_dir):
            filepath = os.path.join(image_dir, filename)
            zipf.write(filepath, arcname=filename)

    zip_buffer.seek(0)  # Reset buffer pointer to start

    # Optional: Clean up image directory after ZIP is generated
    for filename in os.listdir(image_dir):
        file_path = os.path.join(image_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Send ZIP file to the user as a download
    return send_file(zip_buffer, mimetype='application/zip',
                     as_attachment=True, download_name='whirlpool_images.zip')

# Run Flask development server
if __name__ == '__main__':
    app.run(debug=True)
