import torch
print(torch.cuda.is_available())

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
f = '16S_v04_final.csv_Taxonomies.CountedFams.txt_thirty_subset_9.csv'
# Load train
train_val_df = import_data(f)
test_df = import_data(f)
# We're bioinformatics,
# we're not splitting up anything
#train_df, val_df = train_test_split(train_val_df[['text', 'label']], 
#                                    test_size = 0.2, random_state = 42)
# FIXME
#val_df = train_df
tokenizer = AutoTokenizer.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-1000g",
                                          num_labels = len(set(train_val_df['label'])))
tokenized_train = pipeline(train_val_df)
tokenized_val = pipeline(train_val_df)
model = AutoModelForSequenceClassification.from_pretrained("InstaDeepAI/nucleotide-transformer-500m-1000g", 
                                                            trust_remote_code = True, 
                                                            num_labels=len(set(train_val_df['label'])))

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir="./results",
    save_strategy = 'epoch',
    optim="adamw_torch",
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    save_total_limit = 2,
    fp16 = True,
    num_train_epochs=70,
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

trainer.save_model('MODELSAVES')
