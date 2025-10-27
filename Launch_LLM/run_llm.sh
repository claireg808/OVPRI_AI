#!/bin/bash
#SBATCH --gres=gpu:40g:1
#SBATCH --mem=20G
#SBATCH --output=launch_out.log
#SBATCH --qos=short
#SBATCH --job-name=run_llm

source /home/gillaspiecl/OVPRI_AI/Dependencies/venv/bin/activate

export HUGGINGFACE_HUB_TOKEN=$(cat /home/gillaspiecl/OVPRI_AI/Dependencies/.hf_token)
hf auth login --token "$HUGGINGFACE_HUB_TOKEN"

# start vLLM in the background
vllm serve "Llama3.1-8B-I-FP8" \
    --served-model-name llama3-fp8 \
    > vllm_out.log 2>&1 &

echo "Waiting for vLLM to start..."
sleep 60
echo "Launching frontend"

# start frontend
flask --app /home/gillaspiecl/OVPRI_AI/Frontend/flask_session.py run \
    --debug \
    --host=0.0.0.0 \
    --port=5000