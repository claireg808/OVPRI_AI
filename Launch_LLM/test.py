from vllm import LLM, SamplingParams

model = LLM(
    "./Llama3.1-8B-I-FP8",
    tokenizer="meta-llama/Llama-3.1-8B"
)
sampling_params = SamplingParams(max_tokens=256)
outputs = model.generate("What is machine learning?", sampling_params)
for output in outputs:
    print(output.outputs[0].text)