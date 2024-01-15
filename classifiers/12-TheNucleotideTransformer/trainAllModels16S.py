import torch
print(torch.cuda.is_available())
import sys

from transformers import AutoTokenizer
from datasets import Dataset
from transformers import DataCollatorWithPadding
from transformers import TrainingArguments, Trainer, logging
from transformers import AutoModelForSequenceClassification

import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
import logging
from sklearn.model_selection import train_test_split

def import_data(csv_file):
    """
    Import the csv file and get it ready for use. Ensures each file gets the same treatment.
    
    in -> csv_file - string representing the location of the csv file
    out -> pandas dataframe
    """
    df = pd.read_csv(csv_file)
    df.rename(columns = {'sequence': 'text'}, inplace = True)

    return df

def preprocess_function(examples):
    """
    Tokenize the text to create input and attention data
    
    in -> dataset (columns = text, label)
    out -> tokenized dataset (columns = text, label, input, attention)
    """
    return tokenizer(examples["text"], truncation=True)


def pipeline(dataframe):
    """
    Prepares the dataframe so that it can be given to the transformer model
    
    in -> pandas dataframe
    out -> tokenized dataset (columns = text, label, input, attention)
    """    
    # This step isn't mentioned anywhere but is vital as Transformers library only seems to work with this Dataset data type
    dataset = Dataset.from_pandas(dataframe, preserve_index=False)
    tokenized_ds = dataset.map(preprocess_function, batched=True)
    tokenized_ds = tokenized_ds.remove_columns('text')
    return tokenized_ds
print('hi')
#f = '16S_v04_final.csv_Taxonomies.CountedFams.txt_thirty_subset_9.csv'
f = sys.argv[1]
# Load train
train_val_df = import_data(f)
#test_df = import_data(f)

train_df, val_df = train_test_split(train_val_df[['text', 'label']], 
                                    test_size = 0.2, random_state = 42)
tokenizer = AutoTokenizer.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-1000g",
                                          num_labels = len(set(train_val_df['label'])))
print('got to tokenizer')
tokenized_train = pipeline(train_df)
tokenized_val = pipeline(val_df)
model = AutoModelForSequenceClassification.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-1000g", 
                                                            trust_remote_code = True, 
                                                            num_labels=len(set(train_val_df['label'])))
print('got to model')
#model = torch.compile(model)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

#print(f'devices: {torch.cuda.device_count()}')
#print(f'current dev: {torch.cuda.current_device()}')
#print(f'current dev name: {torch.cuda.get_device_name(torch.cuda.current_device())}')
training_args = TrainingArguments(
    output_dir=f"./results_{sys.argv[1].replace('.csv', '')}",
    save_strategy = 'epoch',
    optim="adamw_torch",
    resume_from_checkpoint = True,
    learning_rate=2e-5,
    per_device_train_batch_size=128,
    per_device_eval_batch_size=128,
    save_total_limit = 2,
    fp16 = True,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_steps = 20,
    report_to="none", # Stops transformers from trying to connect to weights and biases site
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

print('training')
trainer.train()
print('done')

trainer.save_model(sys.argv[1] + '_' + 'MODELSAVES')
