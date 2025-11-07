## flask

import os
import sys
import json
from collections import defaultdict
from flask import Flask, request, jsonify

rag_directory = os.path.abspath('/home/gillaspiecl/OVPRI_AI/OVPRI_DocReview') 
redline_directory = os.path.abspath('/home/gillaspiecl/OVPRI_AI/OVPRI_RAG/rag') 
sys.path.append(rag_directory) 
sys.path.append(redline_directory) 
from rag import answer_query 
from redline import redline_document


app = Flask(__name__)
sessions = defaultdict(list)


# RAG
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    session_id = data.get('session_id')

    # save chat history to session
    sessions[session_id].append(user_input)

    response, log_entry = answer_query(
        query=user_input,
        history=sessions[session_id][:-1]
    )

    with open('/home/gillaspiecl/OVPRI_AI/OVPRI_RAG/logs/rag_logs.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')

    return jsonify({'response': response})


# Redline
@app.route('/redline', methods=['POST'])
def redline():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    doc_type = request.form.get('type')

    redlined_text = redline_document(file, doc_type)

    return jsonify({'redline': redlined_text})


# add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response