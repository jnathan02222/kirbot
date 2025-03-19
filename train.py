from datasets import Dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments

# Step 1: Break the text into chunks of 100 lines
def break_text_into_chunks(file_path, chunk_size=100):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines.reverse()

    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk = ''.join(lines[i:i + chunk_size]).strip()
        chunks.append(chunk)
    
    return chunks

file_path = 'dataset.txt'  
chunks = break_text_into_chunks(file_path)

# Step 2: Create a Hugging Face dataset
dataset = Dataset.from_dict({"text": chunks})

# Step 3: Tokenize the dataset using GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

# Apply tokenization to the dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Step 4: Define and train the GPT-2 model
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=4,   # batch size for training
    save_strategy="no"
)

# Initialize the Trainer
trainer = Trainer(
    model=model,                         # the model to train
    args=training_args,                  # training arguments
    train_dataset=tokenized_datasets,    # training dataset
)

# Train the model
trainer.train()

# Step 5: Save the trained model
trainer.save_model("trained_model")  # Saves the model in the directory 'trained_model'
tokenizer.save_pretrained("trained_model")