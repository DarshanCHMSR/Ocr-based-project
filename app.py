#!/usr/bin/env python3
"""
Flask Web Application for PDF Text Extraction and OCR
Provides a web interface for uploading PDFs/images and extracting text with editing capabilities.
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import tempfile
from datetime import datetime
from werkzeug.utils import secure_filename
import json

# Import our extraction modules
try:
    from pdf_text_extractor import extract_text_from_pdf, check_dependencies as check_pdf_deps
    PDF_AVAILABLE = True
    print("✅ PDF processing available")
except ImportError as e:
    PDF_AVAILABLE = False
    print(f"❌ PDF processing not available: {e}")

try:
    import pytesseract
    from PIL import Image, ImageEnhance
    OCR_AVAILABLE = True
    print("✅ OCR processing available")
except ImportError as e:
    OCR_AVAILABLE = False
    print(f"❌ OCR processing not available: {e}")

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_image(image_path, preprocess=True):
    """Extract text from image using OCR."""
    if not OCR_AVAILABLE:
        return "OCR libraries not available. Please install pytesseract and pillow."

    try:
        print(f"Opening image: {image_path}")  # Debug log
        image = Image.open(image_path)
        print(f"Image size: {image.size}, mode: {image.mode}")  # Debug log

        if preprocess:
            # Convert to grayscale and enhance contrast
            image = image.convert('L')
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            print("Image preprocessed")  # Debug log

        # Check if Kannada language is available, fallback to English
        try:
            available_langs = pytesseract.get_languages()
            lang = 'kan' if 'kan' in available_langs else 'eng'
            print(f"Using OCR language: {lang}")  # Debug log
        except:
            lang = 'eng'
            print("Using default language: eng")  # Debug log

        # Extract text using OCR
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(
            image,
            lang=lang,
            config=custom_config
        )

        print(f"OCR completed, text length: {len(extracted_text)}")  # Debug log
        return extracted_text
    except Exception as e:
        error_msg = f"Error processing image: {str(e)}"
        print(error_msg)  # Debug log
        return error_msg


def save_extracted_text(text, original_filename, output_dir=OUTPUT_FOLDER):
    """Save extracted text to a file."""
    base_name = os.path.splitext(original_filename)[0]
    output_filename = f"{base_name}_extracted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Extracted Text from: {original_filename}\n")
            f.write(f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Character Count: {len(text)}\n")
            f.write(f"Word Count: {len(text.split())}\n")
            f.write("=" * 50 + "\n\n")
            f.write(text)
        
        return output_path
    except Exception as e:
        return None


@app.route('/')
def index():
    """Main page with upload form."""
    print("Index route called")  # Debug log
    return render_template('index.html',
                         pdf_available=PDF_AVAILABLE,
                         ocr_available=OCR_AVAILABLE)


@app.route('/test')
def test():
    """Simple test route."""
    return f"""
    <h1>Flask App Test</h1>
    <p>PDF Available: {PDF_AVAILABLE}</p>
    <p>OCR Available: {OCR_AVAILABLE}</p>
    <p>Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}</p>
    <p>Output folder exists: {os.path.exists(OUTPUT_FOLDER)}</p>
    <a href="/">Back to main page</a>
    """


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and text extraction."""
    print(f"Upload route called with method: {request.method}")  # Debug log

    if request.method == 'GET':
        print("GET request to upload, redirecting to index")  # Debug log
        return redirect(url_for('index'))

    print(f"POST request received. Files in request: {list(request.files.keys())}")  # Debug log
    print(f"Form data: {dict(request.form)}")  # Debug log

    if 'file' not in request.files:
        print("No 'file' key in request.files")  # Debug log
        flash('No file selected')
        return redirect(url_for('index'))

    file = request.files['file']
    print(f"File object: {file}, filename: {file.filename}")  # Debug log

    if file.filename == '':
        print("Empty filename")  # Debug log
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        print(f"File is valid and allowed: {file.filename}")  # Debug log

        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        print(f"Saving file to: {filepath}")  # Debug log

        try:
            file.save(filepath)
            print(f"File saved successfully: {filepath}")  # Debug log
        except Exception as e:
            print(f"Error saving file: {e}")  # Debug log
            flash(f'Error saving file: {str(e)}')
            return redirect(url_for('index'))
        
        # Extract text based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()

        try:
            print(f"Processing file: {filename}, extension: {file_ext}")  # Debug log

            if file_ext == 'pdf':
                if not PDF_AVAILABLE:
                    flash('PDF processing not available. Please install required dependencies.')
                    return redirect(url_for('index'))

                method = request.form.get('method', 'auto')
                print(f"Using PDF method: {method}")  # Debug log
                extracted_text = extract_text_from_pdf(filepath, method=method)
            else:
                if not OCR_AVAILABLE:
                    flash('OCR processing not available. Please install required dependencies.')
                    return redirect(url_for('index'))

                preprocess = request.form.get('preprocess', 'true') == 'true'
                print(f"Using OCR with preprocessing: {preprocess}")  # Debug log
                extracted_text = extract_text_from_image(filepath, preprocess=preprocess)

            print(f"Extracted text length: {len(extracted_text) if extracted_text else 0}")  # Debug log

            # Check if extraction was successful
            if not extracted_text or extracted_text.startswith("❌") or extracted_text.startswith("Error"):
                flash(f'Text extraction failed: {extracted_text}')
                if os.path.exists(filepath):
                    os.remove(filepath)
                return redirect(url_for('index'))

            # Save extracted text
            output_path = save_extracted_text(extracted_text, file.filename)

            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)

            print(f"Rendering result page with {len(extracted_text)} characters")  # Debug log

            return render_template('result.html',
                                 text=extracted_text,
                                 filename=file.filename,
                                 output_file=os.path.basename(output_path) if output_path else None,
                                 char_count=len(extracted_text),
                                 word_count=len(extracted_text.split()),
                                 line_count=len(extracted_text.splitlines()))
        
        except Exception as e:
            print(f"Exception during processing: {e}")  # Debug log
            flash(f'Error processing file: {str(e)}')
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('index'))

    else:
        print(f"File not allowed or invalid: {file.filename if file else 'No file'}")  # Debug log
        flash('Invalid file type. Please upload PDF, PNG, JPG, JPEG, GIF, BMP, or TIFF files.')
        return redirect(url_for('index'))


@app.route('/save_edited', methods=['POST'])
def save_edited():
    """Save edited text from Quill editor."""
    try:
        data = request.get_json()
        edited_text = data.get('text', '')
        original_filename = data.get('filename', 'edited_text')
        
        # Save the edited text
        output_path = save_extracted_text(edited_text, f"edited_{original_filename}")
        
        if output_path:
            return jsonify({
                'success': True, 
                'message': 'Text saved successfully!',
                'filename': os.path.basename(output_path)
            })
        else:
            return jsonify({'success': False, 'message': 'Error saving file'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/download/<filename>')
def download_file(filename):
    """Download saved text file."""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))


@app.route('/api/check_dependencies')
def check_dependencies():
    """API endpoint to check available dependencies."""
    deps = {
        'pdf_available': PDF_AVAILABLE,
        'ocr_available': OCR_AVAILABLE
    }
    
    if PDF_AVAILABLE:
        try:
            pdf_deps = check_pdf_deps()
            deps['pdf_details'] = 'All PDF dependencies available'
        except:
            deps['pdf_details'] = 'Some PDF dependencies missing'
    
    if OCR_AVAILABLE:
        try:
            languages = pytesseract.get_languages()
            deps['ocr_languages'] = languages
            deps['kannada_available'] = 'kan' in languages
        except:
            deps['ocr_languages'] = []
            deps['kannada_available'] = False
    
    return jsonify(deps)


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash('File is too large. Maximum size is 16MB.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("🚀 Starting PDF/OCR Text Extraction Web App")
    print("=" * 40)
    print(f"PDF Support: {'✅' if PDF_AVAILABLE else '❌'}")
    print(f"OCR Support: {'✅' if OCR_AVAILABLE else '❌'}")
    print("=" * 40)
    print("📝 Install missing dependencies:")
    if not PDF_AVAILABLE:
        print("   pip install PyPDF2 pdfplumber pdf2image")
    if not OCR_AVAILABLE:
        print("   pip install pytesseract pillow")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
