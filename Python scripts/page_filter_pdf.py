import os
import sys
# Ensure PyPDF2 is installed by running the following command in your terminal:
# pip install PyPDF2


import PyPDF2



# Check if folder path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py /path/to/folder")
    exit()

# Get the folder path from the command-line argument
folder_path = sys.argv[1]

# Verify that the folder exists
if not os.path.isdir(folder_path):
    print(f"Error: {folder_path} is not a valid directory.")
    exit()

# Warn the user and ask for confirmation
print("This script will remove PDF files with fewer than 8 pages from the specified folder.")
print("Please ensure you have backed up your files before proceeding.")
confirmation = input("Do you want to continue? (y/n): ").lower()
if confirmation != 'y':
    print("Operation cancelled.")
    exit()

# List all PDF files in the folder
pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

# Initialize counters
total_pdfs = len(pdf_files)
removed = 0

# Process each PDF file
for pdf in pdf_files:
    file_path = os.path.join(folder_path, pdf)
    try:
        # Open the PDF file in binary read mode
        with open(file_path, 'rb') as file:
            # Create a PdfReader object to read the PDF
            reader = PyPDF2.PdfReader(file)
            # Check if the number of pages is less than 8
            if len(reader.pages) < 8:
                os.remove(file_path)
                removed += 1
                print(f"Removed: {pdf}")
    except PyPDF2.errors.PdfReadError:
        print(f"Invalid PDF: {pdf}")
    except Exception as e:
        print(f"Error processing {pdf}: {e}")

# Print summary
print(f"Total PDFs: {total_pdfs}")
print(f"Removed: {removed}")
print(f"Remaining: {total_pdfs - removed}")