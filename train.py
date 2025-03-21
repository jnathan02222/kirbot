import torch
from transformers import AutoTokenizer,TextDataset,DataCollatorForLanguageModeling,Trainer,TrainingArguments,AutoModelForCausalLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained("gpt2")

def emptyMessage(msg):
    return msg[msg.find(":")+1:].strip() == ''

#Reverse lines and remove empty messages
with open('dataset.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
lines.reverse()
lines = [line for line in lines if not emptyMessage(line)]
with open('dataset_processed.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)

def load_dataset(train_path, tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=128)
 
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset,data_collator
 
train_dataset,data_collator = load_dataset("dataset_processed.txt",tokenizer)

model = AutoModelForCausalLM.from_pretrained("gpt2").to(device)
 
training_args = TrainingArguments(
    output_dir="./result", #The output directory
    overwrite_output_dir=True, #overwrite the content of the output directory
    num_train_epochs=1, # number of training epochs
    per_device_train_batch_size=4, # batch size for training
    warmup_steps=500,# number of warmup steps for learning rate scheduler
    save_strategy="no",
    eval_strategy="no"
)
 
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

trainer.train()
trainer.save_model()

#Improvement ideas
    #Train from scratch on text messages, then fine tune on chat data
    #Use larger model (improved coherence but made personality less accurate)
    #Group conversations together in dataset