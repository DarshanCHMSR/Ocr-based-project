# PDF & OCR Text Extractor Web App

A modern Flask web application for extracting text from PDFs and images with advanced OCR capabilities and rich text editing features.

## Features

### 🚀 Core Functionality
- **PDF Text Extraction**: Multiple extraction methods (PyPDF2, pdfplumber, OCR)
- **Image OCR**: Advanced OCR with Kannada language support
- **Rich Text Editor**: Quill.js-powered editor for text editing
- **Batch Processing**: Process multiple files at once
- **Export Options**: Save edited text as formatted documents

### 🎨 User Interface
- **Modern Design**: Beautiful gradient UI with Bootstrap 5
- **Drag & Drop**: Intuitive file upload with drag-and-drop support
- **Responsive**: Mobile-friendly responsive design
- **Real-time Stats**: Live word/character count and reading time
- **Fullscreen Editor**: Distraction-free editing mode

### 🔧 Technical Features
- **Multiple Extraction Methods**: Auto-detection of best method
- **Image Preprocessing**: Automatic contrast enhancement and grayscale conversion
- **File Management**: Organized file storage and download system
- **Error Handling**: Comprehensive error handling and user feedback
- **Progress Tracking**: Visual progress indicators

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ocr-web-app
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR Engine

#### Windows
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Download Kannada language pack: https://github.com/tesseract-ocr/tessdata

#### macOS
```bash
brew install tesseract
brew install tesseract-lang
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-kan
```

### 4. Create Required Directories
```bash
mkdir uploads outputs
```

## Usage

### 1. Start the Application
```bash
python app.py
```

### 2. Access the Web Interface
Open your browser and navigate to: `http://localhost:5000`

### 3. Upload and Process Files
1. **Upload**: Drag and drop or click to select PDF/image files
2. **Configure**: Choose extraction method and preprocessing options
3. **Extract**: Click "Extract Text" to process the file
4. **Edit**: Use the rich text editor to modify extracted text
5. **Save**: Save edited text as formatted documents

## Supported File Formats

### Input Formats
- **PDFs**: `.pdf`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`

### Output Formats
- **Text Files**: `.txt` with metadata headers
- **Rich Text**: Formatted content with Quill.js

## API Endpoints

### Web Interface
- `GET /` - Main upload page
- `POST /upload` - File upload and processing
- `POST /save_edited` - Save edited text
- `GET /download/<filename>` - Download saved files

### API Endpoints
- `GET /api/check_dependencies` - Check available dependencies

## Configuration

### File Size Limits
- Maximum file size: 16MB
- Configurable in `app.py`: `MAX_CONTENT_LENGTH`

### Processing Options
- **PDF Methods**: Auto, PyPDF2, pdfplumber, OCR
- **Image Preprocessing**: Grayscale conversion, contrast enhancement
- **OCR Language**: Kannada (kan) by default

## File Structure
```
├── app.py                 # Main Flask application
├── pdf_text_extractor.py  # PDF processing module
├── main.py               # Command-line interface
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Upload page
│   └── result.html       # Results and editor page
├── uploads/              # Temporary file storage
├── outputs/              # Saved text files
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Keyboard Shortcuts

### Editor Shortcuts
- `Ctrl+S` / `Cmd+S` - Save edited text
- `Ctrl+F` / `Cmd+F` - Toggle fullscreen editor

## Troubleshooting

### Common Issues

#### 1. Tesseract Not Found
```
TesseractNotFoundError: tesseract is not installed
```
**Solution**: Install Tesseract OCR engine and ensure it's in your PATH.

#### 2. Kannada Language Not Available
```
No Kannada language pack found
```
**Solution**: Install Kannada language pack for Tesseract.

#### 3. PDF Processing Errors
```
PDF dependencies not available
```
**Solution**: Install PDF processing libraries:
```bash
pip install PyPDF2 pdfplumber pdf2image
```

#### 4. Large File Upload Errors
```
File too large (413 error)
```
**Solution**: Reduce file size or increase `MAX_CONTENT_LENGTH` in `app.py`.

### Dependency Check
Visit `/api/check_dependencies` to see available features and missing dependencies.

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Adding New Features
1. **New Extraction Methods**: Add to `pdf_text_extractor.py`
2. **UI Enhancements**: Modify templates in `templates/`
3. **API Extensions**: Add new routes in `app.py`

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
- `FLASK_SECRET_KEY`: Set a secure secret key
- `UPLOAD_FOLDER`: Custom upload directory
- `OUTPUT_FOLDER`: Custom output directory

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the dependency requirements
3. Open an issue on the repository
