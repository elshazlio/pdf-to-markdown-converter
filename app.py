"""
PDF to Markdown Converter with Selective Image OCR
A Streamlit app that converts PDF files to Markdown while preserving text
and running OCR on embedded images.
"""

import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import os
import base64
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class PDFToMarkdownConverter:
    """Handles PDF extraction and Markdown conversion."""
    
    def __init__(self, pdf_bytes, output_dir="output", pdf_name="document"):
        """
        Initialize the converter.
        
        Args:
            pdf_bytes: PDF file content as bytes
            output_dir: Directory to save extracted images
            pdf_name: Name of the PDF file (for organizing output)
        """
        self.pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        self.pdf_name = pdf_name
        self.output_dir = os.path.join(output_dir, pdf_name.replace(".pdf", ""))
        self.image_counter = 0
        
        # Create output directory if it doesn't exist
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def extract_text_blocks(self, page):
        """
        Extract text blocks from a PDF page with position information.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            List of text blocks with position and content
        """
        blocks = page.get_text("dict")["blocks"]
        text_blocks = []
        
        for block in blocks:
            # Only process text blocks (type 0), skip image blocks (type 1)
            if block.get("type") == 0:
                text_content = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text_content += span.get("text", "")
                    text_content += "\n"
                
                if text_content.strip():
                    text_blocks.append({
                        "type": "text",
                        "bbox": block["bbox"],
                        "content": text_content.strip(),
                        "y0": block["bbox"][1]  # Top position for sorting
                    })
        
        return text_blocks
    
    def extract_images(self, page, page_num):
        """
        Extract images from a PDF page.
        
        Args:
            page: PyMuPDF page object
            page_num: Page number for naming
            
        Returns:
            List of image information dictionaries
        """
        image_list = page.get_images()
        images = []
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = self.pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Get image position on page
            img_rects = page.get_image_rects(xref)
            bbox = img_rects[0] if img_rects else (0, 0, 0, 0)
            
            # Save image to file
            self.image_counter += 1
            image_filename = f"image_p{page_num}_{self.image_counter}.{image_ext}"
            image_path = os.path.join(self.output_dir, image_filename)
            pil_image.save(image_path)
            
            images.append({
                "type": "image",
                "bbox": bbox,
                "path": image_path,
                "filename": image_filename,
                "pil_image": pil_image,
                "y0": bbox[1]  # Top position for sorting
            })
        
        return images
    
    def ocr_image(self, pil_image):
        """
        Run OCR on an image using Tesseract.
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            Extracted text or empty string if no text found
        """
        try:
            text = pytesseract.image_to_string(pil_image)
            return text.strip()
        except Exception as e:
            st.warning(f"OCR failed for an image: {str(e)}")
            return ""
    
    def detect_heading(self, text_block):
        """
        Simple heuristic to detect if a text block is likely a heading.
        
        Args:
            text_block: Text block dictionary
            
        Returns:
            Heading level (1-3) or 0 if not a heading
        """
        text = text_block["content"]
        
        # Short text (less than 100 chars) might be a heading
        if len(text) < 100:
            # All caps might be a heading
            if text.isupper() and len(text.split()) <= 10:
                return 1
            # Title case might be a heading
            if text.istitle() and len(text.split()) <= 15:
                return 2
        
        return 0
    
    def format_as_markdown(self, text_block, heading_level=0):
        """
        Format a text block as Markdown.
        
        Args:
            text_block: Text block dictionary
            heading_level: Heading level (0 for regular text)
            
        Returns:
            Formatted Markdown string
        """
        text = text_block["content"]
        
        if heading_level > 0:
            return f"{'#' * heading_level} {text}\n\n"
        else:
            # Regular paragraph
            return f"{text}\n\n"
    
    def convert_to_markdown(self):
        """
        Convert the entire PDF to Markdown.
        
        Returns:
            Markdown string
        """
        markdown_content = []
        
        # Add title
        markdown_content.append(f"# PDF Document Conversion\n\n")
        
        # Process each page
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document[page_num]
            
            # Add page marker for multi-page PDFs
            if len(self.pdf_document) > 1:
                markdown_content.append(f"## Page {page_num + 1}\n\n")
            
            # Extract text blocks and images
            text_blocks = self.extract_text_blocks(page)
            images = self.extract_images(page, page_num + 1)
            
            # Combine and sort by vertical position
            all_elements = text_blocks + images
            all_elements.sort(key=lambda x: x["y0"])
            
            # Process elements in order
            for element in all_elements:
                if element["type"] == "text":
                    # Detect if it's a heading
                    heading_level = self.detect_heading(element)
                    markdown_content.append(
                        self.format_as_markdown(element, heading_level)
                    )
                
                elif element["type"] == "image":
                    # Add image reference
                    markdown_content.append(
                        f"![Image]({element['filename']})\n\n"
                    )
                    
                    # Run OCR on the image
                    ocr_text = self.ocr_image(element["pil_image"])
                    
                    if ocr_text:
                        # Add OCR text as a caption or following paragraph
                        markdown_content.append(
                            f"*Image text (OCR):* {ocr_text}\n\n"
                        )
            
            # Add spacing between pages
            if page_num < len(self.pdf_document) - 1:
                markdown_content.append("---\n\n")
        
        return "".join(markdown_content)
    
    def close(self):
        """Close the PDF document."""
        self.pdf_document.close()


def process_single_pdf(pdf_file):
    """
    Process a single PDF file and return results.
    
    Args:
        pdf_file: Streamlit UploadedFile object
        
    Returns:
        Dictionary with processing results
    """
    try:
        # Read PDF bytes
        pdf_bytes = pdf_file.read()
        pdf_file.seek(0)  # Reset file pointer for potential re-reads
        
        # Create converter
        converter = PDFToMarkdownConverter(pdf_bytes, pdf_name=pdf_file.name)
        
        # Convert to Markdown
        markdown_text = converter.convert_to_markdown()
        
        # Get output directory for this PDF
        output_dir = converter.output_dir
        
        # Close PDF
        converter.close()
        
        return {
            "success": True,
            "filename": pdf_file.name,
            "markdown": markdown_text,
            "output_dir": output_dir,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "filename": pdf_file.name,
            "markdown": None,
            "output_dir": None,
            "error": str(e)
        }


def create_zip_file(results):
    """
    Create a zip file containing all markdown files and images.
    
    Args:
        results: List of processing result dictionaries
        
    Returns:
        Bytes of the zip file
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for result in results:
            if result["success"]:
                # Add markdown file
                md_filename = result["filename"].replace(".pdf", ".md")
                zip_file.writestr(md_filename, result["markdown"])
                
                # Add images if they exist
                output_dir = result["output_dir"]
                if os.path.exists(output_dir):
                    # Create a folder in the zip for this PDF's images
                    folder_name = result["filename"].replace(".pdf", "")
                    for root, dirs, files in os.walk(output_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.join(folder_name, file)
                            zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="PDF to Markdown Converter",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 PDF to Markdown Converter with OCR")
    st.markdown("""
    Upload one or multiple PDF files to convert them to Markdown format. The app will:
    - Preserve original text and formatting (no OCR on text)
    - Extract embedded images
    - Run OCR on images to extract any text they contain
    - Process multiple PDFs in parallel for faster conversion
    - Generate downloadable Markdown files
    """)
    
    # File uploader - now accepts multiple files
    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files to convert to Markdown"
    )
    
    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} file(s): {', '.join([f.name for f in uploaded_files])}")
        
        # Add a convert button
        if st.button("🔄 Convert to Markdown", type="primary"):
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            # Process PDFs in parallel
            with ThreadPoolExecutor(max_workers=min(4, len(uploaded_files))) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(process_single_pdf, pdf_file): pdf_file 
                    for pdf_file in uploaded_files
                }
                
                # Process results as they complete
                completed = 0
                for future in as_completed(future_to_file):
                    result = future.result()
                    results.append(result)
                    
                    completed += 1
                    progress = completed / len(uploaded_files)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing: {completed}/{len(uploaded_files)} files completed")
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            success_count = sum(1 for r in results if r["success"])
            failure_count = len(results) - success_count
            
            if success_count > 0:
                st.success(f"✅ Successfully converted {success_count} file(s)!")
            if failure_count > 0:
                st.error(f"❌ Failed to convert {failure_count} file(s)")
            
            # Show results for each file
            for result in results:
                if result["success"]:
                    with st.expander(f"📝 {result['filename']}", expanded=False):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.code(result["markdown"][:1000] + "..." if len(result["markdown"]) > 1000 else result["markdown"], 
                                   language="markdown")
                        
                        with col2:
                            # Individual download button
                            md_filename = result["filename"].replace(".pdf", ".md")
                            st.download_button(
                                label="⬇️ Download",
                                data=result["markdown"],
                                file_name=md_filename,
                                mime="text/markdown",
                                key=f"download_{result['filename']}"
                            )
                            
                            # Show image count
                            if os.path.exists(result["output_dir"]):
                                image_count = len([f for f in os.listdir(result["output_dir"]) 
                                                 if f.endswith(('.png', '.jpg', '.jpeg'))])
                                st.metric("Images", image_count)
                else:
                    with st.expander(f"❌ {result['filename']} - Failed", expanded=False):
                        st.error(f"Error: {result['error']}")
            
            # Download all as ZIP
            if success_count > 0:
                st.divider()
                st.subheader("📦 Download All")
                
                # Let user customize ZIP filename
                col1, col2 = st.columns([3, 1])
                with col1:
                    zip_filename = st.text_input(
                        "ZIP filename",
                        value="converted_pdfs.zip",
                        help="Customize the name of your ZIP file",
                        key="zip_filename"
                    )
                    # Ensure .zip extension
                    if not zip_filename.endswith('.zip'):
                        zip_filename += '.zip'
                
                try:
                    zip_data = create_zip_file([r for r in results if r["success"]])
                    st.download_button(
                        label="⬇️ Download All as ZIP (Markdown + Images)",
                        data=zip_data,
                        file_name=zip_filename,
                        mime="application/zip",
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"Error creating ZIP file: {str(e)}")
            
            # Show all extracted images
            st.divider()
            st.subheader("🖼️ All Extracted Images")
            
            all_images = []
            for result in results:
                if result["success"] and os.path.exists(result["output_dir"]):
                    for img_file in os.listdir(result["output_dir"]):
                        if img_file.endswith(('.png', '.jpg', '.jpeg')):
                            all_images.append({
                                "path": os.path.join(result["output_dir"], img_file),
                                "name": img_file,
                                "pdf": result["filename"]
                            })
            
            if all_images:
                cols = st.columns(3)
                for idx, img_info in enumerate(all_images):
                    with cols[idx % 3]:
                        st.image(img_info["path"], 
                               caption=f"{img_info['pdf']}: {img_info['name']}", 
                               use_container_width=True)
            else:
                st.info("No images were extracted from the PDFs.")
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("ℹ️ Instructions")
        st.markdown("""
        ### How to use:
        1. Upload one or multiple PDF files
        2. Click "Convert to Markdown"
        3. Wait for parallel processing
        4. Preview outputs and download individually or as ZIP
        
        ### Requirements:
        - Tesseract OCR must be installed on your system
        - For macOS: `brew install tesseract`
        - For Ubuntu: `apt-get install tesseract-ocr`
        - For Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
        
        ### Features:
        - ✅ **Batch processing** - Upload multiple PDFs
        - ✅ **Parallel conversion** - Process up to 4 PDFs simultaneously
        - ✅ Preserves original text (no OCR on text)
        - ✅ Extracts images with OCR
        - ✅ Maintains document structure
        - ✅ Detects headings
        - ✅ Individual or bulk downloads (ZIP)
        - ✅ Progress tracking
        """)
        
        st.header("🔧 About")
        st.markdown("""
        Built with:
        - **Streamlit** - Web UI
        - **PyMuPDF** - PDF parsing
        - **Tesseract** - OCR engine
        - **Pillow** - Image processing
        - **ThreadPoolExecutor** - Parallel processing
        """)


if __name__ == "__main__":
    main()

