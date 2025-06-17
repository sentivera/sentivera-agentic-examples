import os
from PyPDF2 import PdfReader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_pdf_to_text(pdf_path, output_dir=None, password=None):
    """
    Convert a PDF file to text and save it to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str, optional): Directory to save the text file. If None, uses the same directory as the PDF.
        password (str, optional): Password for encrypted PDFs
    """
    try:
        # Create output directory if it doesn't exist
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Determine output path
        if output_dir:
            output_path = os.path.join(output_dir, f"{base_name}.txt")
        else:
            output_path = os.path.join(os.path.dirname(pdf_path), f"{base_name}.txt")
        
        # Read PDF file
        logging.info(f"Reading PDF file: {pdf_path}")
        reader = PdfReader(pdf_path)
        
        # Check if PDF is encrypted
        if reader.is_encrypted:
            if password:
                reader.decrypt(password)
            else:
                logging.warning(f"PDF is encrypted but no password provided: {pdf_path}")
                return False
        
        # Extract text from all pages
        text_content = []
        for page in reader.pages:
            text_content.append(page.extract_text())
        
        # Combine all text
        full_text = "\n".join(text_content)
        
        # Write to text file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        logging.info(f"Successfully converted PDF to text: {output_path}")
        return True
        
    except Exception as e:
        logging.error(f"Error converting PDF {pdf_path}: {str(e)}")
        return False

def process_directory(directory_path, output_dir=None, password=None):
    """
    Process all PDF files in a directory.
    
    Args:
        directory_path (str): Path to the directory containing PDF files
        output_dir (str, optional): Directory to save the text files
        password (str, optional): Password for encrypted PDFs
    """
    success_count = 0
    fail_count = 0
    
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            if convert_pdf_to_text(pdf_path, output_dir, password):
                success_count += 1
            else:
                fail_count += 1
    
    logging.info(f"Conversion complete. Successfully converted: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    # Directory containing PDF files
    pdf_dir = os.path.join(os.path.dirname(__file__), "files")
    
    # Create output directory for text files
    output_dir = os.path.join(os.path.dirname(__file__), "text_output")
    
    # Process all PDF files in the directory
    process_directory(pdf_dir, output_dir)
