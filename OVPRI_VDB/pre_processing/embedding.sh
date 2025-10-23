#!/bin/bash
#SBATCH --gres=gpu:40g:1
#SBATCH --mem=100G
#SBATCH --output=emb_out.log
#SBATCH --qos=short
#SBATCH --job-name=embed

source /home/gillaspiecl/OVPRI_VDB/vdb_venv/bin/activate

python embedding.py