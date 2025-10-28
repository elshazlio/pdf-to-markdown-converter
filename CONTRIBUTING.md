# Contributing to PDF to Markdown Converter

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, Tesseract version)
- Sample PDF (if possible and not confidential)

### Suggesting Features

Have an idea? Open an issue with:
- Clear description of the feature
- Use case and benefits
- Any implementation ideas (optional)

### Pull Requests

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR-USERNAME/pdf2md-app.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes** and test thoroughly
5. **Commit**: `git commit -m "Add feature: your feature description"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Open a Pull Request** with a clear description

### Development Setup

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/pdf2md-app.git
cd pdf2md-app

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and modular

### Testing

Before submitting:
- Test with various PDF types (text-heavy, image-heavy, mixed)
- Test single and multiple file uploads
- Verify OCR functionality works
- Check that downloads work correctly

## Questions?

Feel free to open an issue for any questions about contributing!

---

**Thank you for making this project better!** ❤️

