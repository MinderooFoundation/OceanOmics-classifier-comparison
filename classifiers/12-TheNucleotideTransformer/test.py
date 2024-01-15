import torch
print(torch.cuda.is_available())
import glob

from transformers import AutoTokenizer
from datasets import Dataset
from transformers import DataCollatorWithPadding
from transformers import TrainingArguments, Trainer, logging
from transformers import AutoModelForSequenceClassification

import pandas as pd
import numpy as np
import logging

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

for m in glob.glob('*MODELSAVES'):
    model = AutoModelForSequenceClassification.from_pretrained(m)
    tokenizer = AutoTokenizer.from_pretrained(m)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    trainer = Trainer(model=model, tokenizer = tokenizer, data_collator=data_collator)

    # model = AutoModelForSequenceClassification.from_pretrained('./12s_v010_final.csv_MODELSAVES')
    id_dict_f = 'ID_DICTS/' + m.replace('_MODELSAVES', '').replace('.csv','_id_dict.csv')
    print(id_dict_f)
    print('hi')
    id_dict = {}
    #for line in open('12s_v010_final_id_dict.csv'):
    for line in open(id_dict_f):
        taxid, thisid = line.split()
        id_dict[int(thisid)] = taxid

    for f in glob.glob('INPUT/*fa.csv'):
        #f = glob.glob('*fa.csv')[0]
        print(f)
        test_df = import_data(f)
        tokenized_test = pipeline(test_df)
        #preds = trainer.predict(tokenized_test)
        preds = trainer.predict(tokenized_test)
        scores = np.max(torch.nn.functional.softmax(torch.tensor(preds[0]), dim=-1).numpy(), axis=1)
        #probas = trainer.model.predict_proba(tokenized_test)
        #print(probas[:10])
        preds_flat = [np.argmax(x) for x in preds[0]]
        taxid_preds = [id_dict[thisid] for thisid in preds_flat]
        test_df['predictions'] = taxid_preds
        test_df['scores' ] = scores
        test_df.to_csv(f + '_vs_' + m + '.predictions.csv')
            
