from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

model_name = "mistralai/Mistral-7B-Instruct-v0.1"

dataset = load_dataset("json", data_files="dataset.jsonl")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def tokenize(examples):
    return tokenizer(
        [f"{x['prompt']}\n###\n{x['completion']}" for x in examples['data']],
        truncation=True,
        padding="max_length",
        max_length=512
    )

tokenized_dataset = dataset.map(tokenize, batched=True)

args = TrainingArguments(
    output_dir="./checkpoints",
    per_device_train_batch_size=1,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=100,
    fp16=True
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator
)

trainer.train()
