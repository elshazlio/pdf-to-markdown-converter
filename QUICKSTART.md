# Quick Start Guide

Get the PDF to Markdown converter running in 5 minutes!

## Step 1: Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update && sudo apt-get install tesseract-ocr
```

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install and add to PATH

## Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the App

**Easy way (recommended):**
```bash
./run.sh
```

**Manual way:**
```bash
source venv/bin/activate
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

> **Note:** After the initial setup, you only need to run `./run.sh` each time you want to use the app!

## Step 5: Convert Your PDFs

1. Click "Browse files" and select one or multiple PDFs
2. Click "Convert to Markdown"
3. Watch the progress bar as PDFs are processed in parallel
4. Preview each output in expandable sections
5. Download individually or click "Download All as ZIP"

Done! 🎉

### Batch Processing Tips

- **Multiple files**: Select multiple PDFs at once for batch conversion
- **Parallel processing**: Up to 4 PDFs process simultaneously
- **ZIP download**: Get all Markdown files and images in one ZIP file
- **Individual downloads**: Each PDF has its own download button

## Troubleshooting

**"Tesseract not found"**
- Verify installation: `tesseract --version`
- Add to PATH if needed

**"Module not found"**
- Ensure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

**App won't start**
- Check port 8501 is available
- Use custom port: `streamlit run app.py --server.port 8502`

## Tips

- **Batch conversion**: Upload 10+ PDFs at once for efficient processing
- Higher quality PDFs = better OCR results
- Images with clear text work best
- Check the `output/` folder for organized extracted images
- Each PDF gets its own folder in `output/`
- Preview before downloading to verify output
- Use ZIP download for multiple PDFs to save time

Need more help? Check `README.md` for detailed documentation.

