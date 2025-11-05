# 📄 PDF to Markdown Converter with Selective Image OCR

A Python web application built with Streamlit that converts PDF files to Markdown format while preserving original text and running OCR on embedded images.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Convert single or multiple PDFs to Markdown with parallel processing, automatic OCR on images, and bulk download as ZIP!

## Features

✨ **Key Features:**
- 📄 Upload and parse single or multiple PDF files
- 🚀 **Parallel processing** - Convert up to 4 PDFs simultaneously for faster batch conversion
- 📝 Preserve original text and formatting (no OCR on text)
- 🖼️ Extract embedded images from PDFs
- 🔍 Run Tesseract OCR on images to extract text
- 📋 Generate well-formatted Markdown output
- ⬇️ Download individual Markdown files or bulk download as ZIP
- 📊 Real-time progress tracking
- 🎯 Automatic heading detection
- 📁 Maintain document structure and layout

## Prerequisites

### Install Tesseract OCR

Tesseract must be installed on your system before running the app.

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Windows:**
1. Download the installer from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer
3. Add Tesseract to your PATH

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### First Time Setup

1. **Navigate to the project directory:**
```bash
cd path/to/PDF2MD-App
```

2. **Run the launch script (it will auto-setup):**
```bash
./run.sh
```

The script will automatically create the virtual environment and install dependencies on first run.

### Every Time After

Just run:
```bash
./run.sh
```

That's it! The app will open automatically at `http://localhost:8501`

### Alternative (Manual Method)

If you prefer to run manually:
```bash
source venv/bin/activate
streamlit run app.py
```

2. **Open your browser** - Streamlit will automatically open at `http://localhost:8501`

3. **Upload one or more PDF files** using the file uploader (supports multiple files)

4. **Click "Convert to Markdown"** to process the PDFs (they'll be processed in parallel)

5. **Monitor progress** with the real-time progress bar

6. **Preview outputs** for each PDF in expandable sections

7. **Download files** - either individually or all at once as a ZIP file

## How It Works

### PDF Processing Pipeline

1. **Upload**: User uploads one or more PDF files through the Streamlit interface
2. **Parallel Processing**: Up to 4 PDFs are processed simultaneously using ThreadPoolExecutor
3. **Text Extraction**: PyMuPDF extracts text blocks with position information from each PDF
4. **Image Extraction**: PyMuPDF extracts embedded images and saves them to organized directories
5. **OCR Processing**: Tesseract runs OCR on each extracted image
6. **Layout Reconstruction**: Elements are sorted by vertical position to maintain reading order
7. **Markdown Generation**: Text and images are combined into well-formatted Markdown for each PDF
8. **Output**: User can preview each result and download individually or as a ZIP bundle

### Text Handling

- Original PDF text is extracted directly (no OCR on text content)
- Text formatting and structure are preserved
- Automatic heading detection based on text properties:
  - Short, all-caps text → Level 1 heading
  - Title case text → Level 2 heading
  - Regular text → Paragraphs

### Image Handling

- Images are extracted and saved to the `output/` directory
- Each image is processed through Tesseract OCR
- If text is detected in the image, it's added as an italic caption
- Image references use relative paths in the Markdown

## Project Structure

```
PDF2MD App/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Comprehensive documentation
├── QUICKSTART.md      # Quick setup guide
├── sample_output.md   # Example output
├── run.sh             # Launch script
├── .gitignore         # Git ignore rules
└── output/            # Directory for extracted images (created automatically)
    ├── document1/     # Images from document1.pdf
    ├── document2/     # Images from document2.pdf
    └── ...
```

## Dependencies

- **Streamlit** (≥1.28.0) - Web application framework
- **PyMuPDF** (≥1.23.0) - PDF parsing and extraction
- **Pillow** (≥10.0.0) - Image processing
- **pytesseract** (≥0.3.10) - Python wrapper for Tesseract OCR

## Example Output

Given a PDF with text and images, the output Markdown will look like:

```markdown
# PDF Document Conversion

## Page 1

# MAIN TITLE

This is a paragraph of text extracted from the PDF. The original formatting is preserved.

![Image](image_p1_1.png)

*Image text (OCR):* Text extracted from the image via OCR appears here.

## Another Heading

More content follows...

---
```

## Limitations & Notes

- **OCR Accuracy**: OCR quality depends on image resolution and clarity
- **Layout Complexity**: Very complex PDF layouts may not convert perfectly
- **Local Only**: This app runs locally and doesn't require internet connection
- **No LLMs/APIs**: Uses only open-source libraries for processing
- **Image Formats**: Supports common image formats (PNG, JPEG, etc.)

## Troubleshooting

### "Tesseract not found" error
- Make sure Tesseract is installed and in your system PATH
- On Windows, you may need to specify the Tesseract path:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### Poor OCR results
- OCR accuracy depends on image quality
- Try using higher resolution PDFs
- Ensure images contain clear, readable text

### Memory issues with large PDFs
- Process PDFs page by page if needed
- Close and reopen the app to free memory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- ⭐ Star this repo if you find it useful!

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues with:
- **Streamlit**: [Streamlit Documentation](https://docs.streamlit.io/)
- **PyMuPDF**: [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- **Tesseract**: [Tesseract Documentation](https://github.com/tesseract-ocr/tesseract)
