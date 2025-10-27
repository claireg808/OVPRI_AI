## Produce a revised "redlined" version of a user's provided document

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


llm = ChatOpenAI(
    base_url=os.environ['BASE_URL'],
    api_key='dummy-key',
    model=os.environ['MODEL']
)


# read in checklist
with open('Data/CDA_Checklist.txt', 'r', encoding='utf-8') as f:
        checklist = f.read()


def redline(document, type):
    # generate prompt
    with open('doc_review_prompt.txt', 'r', encoding='utf-8') as f:
        prompt_template_txt = f.read()

    if type == 'Confidentiality Agreement':
        full_prompt = prompt_template_txt \
                    .replace('{CHECKLIST}', checklist) \
                    .replace('{DOCUMENT}', document)
    
    # invoke LLM
    response = llm.invoke(full_prompt).content

    return response