## Produce a revised "redlined" version of a user's provided document

import io
import os
import re
import magic
import docx2txt
from docx import Document
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pdfminer.high_level import extract_text


load_dotenv()

# initialize LLM
llm = ChatOpenAI(
    base_url=os.environ['BASE_URL'],
    api_key='dummy-key',
    model=os.environ['MODEL'],
    temperature=0.2
)

# read checklist
with open('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview/data/CDA_Checklist.txt', 'r', encoding='utf-8') as f:
    checklist = f.read()

# read policy
with open('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview/data/Corporate_Research_Agreements_Policy.txt', 'r', encoding='utf-8') as f:
    policy = f.read()

# read redline prompt
with open('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview/doc_review_prompt.txt', 'r', encoding='utf-8') as f:
    redline_prompt_txt = f.read()

# read redline prompt
with open('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview/second_pass_prompt.txt', 'r', encoding='utf-8') as f:
    revision_prompt_txt = f.read()

# format as doc
def format(text):
    document = Document()

    title = text.split('\n')[0]

    document.add_heading(title, level=1)

    body_text = text.split('\n')[1:]

    for paragraph in body_text:
        document.add_paragraph(paragraph)

    return document


# produce redline version of uploaded document
def redline_document(document, type):
    # read document type and reset file pointer
    file_type = magic.from_buffer(document.read(2048))
    document.seek(0)

    if 'pdf' in file_type.lower():  # .pdf
        pdf_bytes = io.BytesIO(document.read())
        text = extract_text(pdf_bytes)
    else:  # .docx
        try:
            text = docx2txt.process(document)
        except:
            return 'Please upload in either .pdf or .docx format.', {'error': 'Incorrect file type'}

    # generate redline prompt
    words = str(int(len(text.split()) * 1.2))
    if type == 'Confidentiality Agreement':
        redline_prompt = redline_prompt_txt \
                    .replace('{POLICIES}', policy) \
                    .replace('{CHECKLIST}', checklist) \
                    .replace('{DOCUMENT}', text) \
                    .replace('{WORDS}', words)
    
        # invoke LLM for redlined section
        redline = llm.invoke(redline_prompt).content

        revision_prompt = revision_prompt_txt \
                    .replace('{POLICIES}', policy) \
                    .replace('{CHECKLIST}', checklist) \
                    .replace('{DOCUMENT}', redline) \
                    .replace('{WORDS}', words)
        
        final_review = llm.invoke(revision_prompt).content

    redline_doc = format(redline)
    final_doc = format(final_review)

    redline_doc.save('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview/data/AI_Redline_Test.docx')
    final_doc.save('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview/data/AI_Redline_Final_Test.docx')

    return final_review