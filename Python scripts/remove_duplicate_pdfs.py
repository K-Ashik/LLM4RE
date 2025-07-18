import os
import re

def normalize_filename(filename):
    """Normalize filename by removing specific duplicate indicators."""
    base_name, ext = os.path.splitext(filename)
    normalized_base = re.sub(r'(\s+[2-9]+|\(\d+\)|[\(\[]?copy[\)\]]?|_copy)', '', base_name, flags=re.IGNORECASE)
    return normalized_base.lower().strip()

# Define the folder path
folder_path = "/Users/rising.volkan007/Desktop/duplicates_filter_code/Duplicate_removing"

# List all PDF files in the folder (case-insensitive and only regular files)
pdf_files = [
    f for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.pdf')
]

# Sort files to prioritize originals (no trailing numbers) over duplicates (with numbers)
pdf_files.sort(key=lambda x: (bool(re.search(r'\s+[2-9]+|\(\d+\)|[\(\[]?copy[\)\]]?|_copy', x)), x))

# Initialize data structures
seen_names = set()
duplicates = []

# Identify duplicates based on normalized filenames
for file in pdf_files:
    file_path = os.path.join(folder_path, file)
    normalized_name = normalize_filename(file)
    if normalized_name in seen_names:
        duplicates.append(file_path)
    else:
        seen_names.add(normalized_name)

# Remove duplicate files
for duplicate in duplicates:
    try:
        os.remove(duplicate)
        print(f"Removed duplicate file: {duplicate}")
    except Exception as e:
        print(f"Error removing {duplicate}: {e}")

# Print summary of the operation
print("Running in name-based mode (comparing normalized filenames)")
print(f"Total PDF files: {len(pdf_files)}")
print(f"Unique PDF files: {len(seen_names)}")
print(f"Duplicates removed: {len(duplicates)}")