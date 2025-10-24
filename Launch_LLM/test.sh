#!/bin/bash
#SBATCH --gres=gpu:40g:1
#SBATCH --mem=20G
#SBATCH --output=launch_out.log
#SBATCH --qos=short
#SBATCH --job-name=run_llm

source /home/gillaspiecl/OVPRI_AI/Dependencies/venv/bin/activate

python test.py