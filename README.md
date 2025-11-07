# OVPRI AI Assistants
### This repository contains the OVPRI AI Assistants project

Note: BASH scripts are written for running on the HPC server Hickory

# Running the Website

To run the LLM and launch the backend, submit the script 'run_llm.sh':  
> sbatch Launch_LLM/run_llm.sh

To launch the frontend:
> cd Frontend
> npm run dev

On your local machine's terminal, open a port into Hickory:  
* Note: Do not close the terminal window.  
> ssh -L 5001:localhost:5000 your-vcu-username@hickory.cs.vcu.edu

Access the website at the local URL.

# Backend Setup

## Initial Set Up
To run this project, create a new Python virtual environment and install the dependencies in 'requirements.txt':
> python -m venv venv_name  
> source venv_name/bin/activate  
> pip install -r requirements.txt  

## RAG
The RAG tool creates the Chatbot portion of the website

### Pre-Processing
To convert .pdf and .docx documents to .txt, run 'convert_formats.py':  
* Note: Either change the expected path name, or store your source documents under 'OVPRI_RAG/data/HRPP'.
> python convert_formats.py

To normalize these documents, run 'normalize.py':  
> python normalize.py

To embed these documents into a local Chroma Vector Database, launch the LLM and run 'embedding.py':  
> sbatch Launch_LLM/run_llm.sh  
> sbatch OVPRI_RAG/pre_processing/embedding.sh  

## Redline
The Redline tool creates the Document Review portion of the website
* Ensure the approproate policies and checklists are stored in OVPRI_DocReview/data