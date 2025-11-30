import re
from pypdf import PdfReader

# read pdf
reader = PdfReader('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview/data/RV00036073_Original_CDA.pdf')

# Get the total number of pages in the PDF
num_pages = len(reader.pages)
print(f"Number of pages: {num_pages}")

# Access a specific page (e.g., the first page, which is at index 0)
page = reader.pages[0]

# Extract text from the page
text = page.extract_text()