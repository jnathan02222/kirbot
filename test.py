from transformers import pipeline
 
generator = pipeline('text-generation', model='./result', tokenizer='gpt2', max_length=800, truncation=True)
 
result = generator('darren2427: bager you fatfuck\nbadger555: ')[0]['generated_text']

print(result)