from transformers import pipeline
 
generator = pipeline('text-generation', model='./result', tokenizer='gpt2', max_length=800)
 
result = generator('darren2427: ')[0]['generated_text']
