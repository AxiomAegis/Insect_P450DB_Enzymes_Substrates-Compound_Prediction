#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.environ["CUDA_VISIBLE_DEVICES"]="1"


# In[2]:


import sys
sys.path.insert(0, 'code')
from prediction import ESP_predicton


# In[14]:


import pandas as pd
data = pd.read_csv("/datb/yangbing/project/LLM/insect-cytochrome-p450-database-enzymes-substrates-compound-prediction/data/training_data/train_val_p450/test.csv").drop_duplicates()
data


# In[13]:


def calculate_ESP_predicton(row):
    pred_df = ESP_predicton(
        metabolite_list = [row["SMILES"]],
        enzyme_list = [row["Protein sequence"]]
             )
    
    if pred_df is not None:
        return pred_df.loc[0, "valid input"], pred_df.loc[0, "Prediction score"]
    else:
        return "No result", "No result"

data[['valid input', "Prediction score"]] = data.apply(calculate_ESP_predicton, axis=1, result_type="expand")
data


# In[6]:


data.to_excel('P450_train_val_p450-test.csv.xlsx', index=False)


# In[ ]:




