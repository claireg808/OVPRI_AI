## Chunk documents into max 1024 tokens per chunk
## Create embedding representation
## Attach metadata for each chunk
    # Document name
    # Document date
    # Chunk ID
    # Text
    # Embedding

import os
import re
import shutil
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from llama_index.core.node_parser import (
    SemanticDoubleMergingSplitterNodeParser,
    LanguageConfig,
)
from llama_index.core import SimpleDirectoryReader


load_dotenv()

# initialize llm
llm = ChatOpenAI(
    base_url=os.environ['BASE_URL'],
    api_key='dummy-key',
    model=os.environ['MODEL']
)


# create document summary specific to a given chunk
def summarize_document(context, chunk):
    prompt = "{PRIOR_TEXT} Here is the text we want to situate given the previous content:{CHUNK_CONTENT} " \
    "Please give a short succinct context to situate this text within the overall document for the purposes of improving search retrieval and understanding of the text. " \
    "Answer only with the succinct context and nothing else."

    full_prompt = prompt \
            .replace('{PRIOR_TEXT}', context) \
            .replace('{CHUNK_CONTENT}', chunk)
    
    summary = llm.invoke(full_prompt).content

    return summary
    
# combine chunk data
def assemble_chunks(chunks, embeddings, doc_name, doc_date):
    chunked_records = []
    for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        chunked_records.append({
            'text': chunk,
            'embedding': vector, 
            'metadata': {
                'chunk_number': idx,
                'document_name': doc_name,
                'effective_date': doc_date
            }
        })

    return chunked_records


# convert assembled chunks to langchain Documents
def records_to_documents(chunk_lists):
    docs = []
    for chunk_list in chunk_lists:
        for record in chunk_list:
            docs.append(
                Document(
                    page_content=record['text'],
                    metadata=record['metadata']
                )
            )
    return docs

# extract the date of document revision
def extract_revision_date(doc_name: str, file_text: str) -> str:
    # list of documents to skip
    skip = ['HRP General Documents', 'HRP Templates']

    # check the start for the revision date
    date_at_start_match = re.search(r"^[a-z]*-[0-9]*[a-z]? \|\s*(\d{1,2}\/\d{1,2}\/\d{4})", file_text, re.IGNORECASE)
    if date_at_start_match:
        date = date_at_start_match.group(1)
        formatted_date = datetime.strptime(date, '%m/%d/%Y').strftime('%m/%d/%Y')
        return formatted_date
    
    # list of possible identifications for the revision date
    list_of_date_formats = [
        "revised:?\s*(\d{1,2}\/\d{1,2}\/\d{4})",
        "revision\s*(?:date)?:?\s*(\d{1,2}\/\d{1,2}\/\d{4})"
    ]

    # find all revision dates in the document
    doc_date_matches = []
    for rgx in list_of_date_formats:
        doc_date_matches.extend(re.findall(rgx, file_text, re.IGNORECASE))

    # if no revision date is found
    if not doc_date_matches or doc_name in skip:
        print(f'[INFO] No revision date found: {doc_name}')
        return 'Unknown'

    # convert to datetime objects and sort
    doc_date_series = pd.Series(doc_date_matches)
    sorted_dates = doc_date_series.apply(pd.to_datetime, format='%m/%d/%Y').sort_values()
    # choose latest date
    final_date = sorted_dates.iloc[-1].strftime('%m/%d/%Y')

    return final_date

# delete the Chroma collection if it already exists
def delete_collection(directory):
    try:
        shutil.rmtree(directory)
        print(f'[INFO] Previous Chroma database deleted successfully.')
    except Exception as e:
        print(f'[INFO] Did not delete collection: {e}')


if __name__ == '__main__':
    folder = '/home/gillaspiecl/OVPRI_VDB/data/HRPP_normalized'
    reader = SimpleDirectoryReader(input_dir=folder)
    text_files = reader.load_data()

    # initialize embedding model: 1024d
    embed_model_name = os.environ['EMBEDDING_MODEL']
    embedding_model = HuggingFaceEmbeddings(model_name=embed_model_name)

    # initialize splitter
    config = LanguageConfig(language='english', spacy_model='en_core_web_lg')
    splitter = SemanticDoubleMergingSplitterNodeParser(
        language_config=config,
        initial_threshold=0.4,
        appending_threshold=0.2,
        merging_threshold=0.3
    )

    complete_chunks = []
    for file in text_files:
        file_path = file.metadata.get('file_path', None)
        doc_name = os.path.splitext(os.path.basename(file_path))[0]

        print(f'[INFO] Embedding {doc_name}')

        full_text = file.get_content()
        doc_date = extract_revision_date(doc_name, full_text)
        chunks = splitter.get_nodes_from_documents([file])

        chunks_and_summaries = []
        for idx, chunk in enumerate(chunks):
            chunk = chunk.get_content()

            # get context of last 10 chunks
            start = max(0, idx-10)
            previous_text = ''
            for text_node in chunks[start:idx]:
                text = text_node.get_content()
                previous_text += text + '\n'
            summary = summarize_document(previous_text, chunk)
            text = 'Summary: ' + summary + '\n Chunk: ' + chunk
            chunks_and_summaries.append(text)

        embeddings = embedding_model.embed_documents(chunks_and_summaries)

        # add metadata
        doc_complete_chunks = assemble_chunks(chunks_and_summaries, embeddings, doc_name, doc_date)
        complete_chunks.append(doc_complete_chunks)

    # convert records to LangChain Documents
    docs = records_to_documents(complete_chunks)

    # create or update Chroma DB
    collection_name = 'hrpp_docs'
    directory = '/home/gillaspiecl/OVPRI_VDB/data/chroma_db'
    delete_collection(directory)
    vectorstore = Chroma.from_documents(
        documents=docs,
        collection_name=collection_name,
        embedding=embedding_model,
        persist_directory=directory
    )

    print('[INFO] Chroma DB built and persisted.')

    with open('/home/gillaspiecl/OVPRI_VDB/logs/embedding_3.txt', 'w', encoding='utf-8') as f:
        for doc in docs:
            f.write(str(doc.page_content) + '\n\n')