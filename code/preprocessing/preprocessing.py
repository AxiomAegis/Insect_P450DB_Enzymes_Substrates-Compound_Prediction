import os
from os.path import join
import argparse
import pandas as pd

from smiles_embeddings import *
from protein_embeddings import *

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_val_path",
        type=str,
        required=True,
        help="Path, where train, test, and validation dataset are as csv files",
    )
    parser.add_argument(
        "--outpath",
        type=str,
        required=True,
        help="Path, where the protein and SMILES embeddings should be saved.",
    )
    parser.add_argument(
        "--prot_emb_no",
        default=2000,
        type=int,
        help="Number of protein sequences in one dictionary.",
    )
    parser.add_argument(
        "--smiles_emb_no",
        default=2000,
        type=int,
        help="Number of SMILES strings in one dictionary.",
    )
    return parser.parse_args()
args = get_arguments()



# #Find all training and validation dataframes
# dataframes = os.listdir(args.train_val_path)
# df = pd.read_csv(join(args.train_val_path, dataframes[0]))
# for dataframe in dataframes[1:]:
# 	df = df.append(pd.read_csv(join(args.train_val_path, dataframe)), ignore_index = True)

# 创建文件夹
def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
create_dir_not_exist(join(args.outpath, "SMILES"))
create_dir_not_exist(join(args.outpath, "Protein"))

# 只列出数据框文件 
import glob
all_matches = glob.glob(f'{args.train_val_path}/*')
# 使用列表推导式和 os.path.isfile 过滤出仅是文件的项
dataframes = [f for f in all_matches if os.path.isfile(f)]

# dataframes = glob.glob(f'{args.train_val_path}/*')
df = pd.read_csv(dataframes[0])
for dataframe in dataframes[1:]:
	df = df._append(pd.read_csv(dataframe), ignore_index = True)


#Get all Protein Sequences and SMILES strings
all_sequences = list(set(df["Protein sequence"]))
all_smiles = list(set(df["SMILES"]))
print("No. of different sequences: %s, No. of different SMILES strings: %s" % (len(all_sequences), len(all_smiles)))

try:
	os.mkdir(args.outpath)
except:
	pass

print("Calculating protein embeddings:")
calculate_protein_embeddings(all_sequences, args.outpath, args.prot_emb_no)
print("Calculating SMILES embeddings:")
calculate_smiles_embeddings(all_smiles, args.outpath, args.smiles_emb_no)