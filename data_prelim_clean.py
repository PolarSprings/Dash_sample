import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import *


repo = 'C:/Users/benno/OneDrive/Python/NYCDSA/Final project/Datasets/a.csv'

columns = ['word','year','match_count','volume_count']

df = pd.read_csv(repo, skipinitialspace=False,sep='\t',names=columns)




# for i in range(1,10):
# 	tup = (i,[j for j in df.word.values if len(j) == i])
# 	e_all_lengths.append(tup)

leng = []
val = []

for i in df.word.values:

	i = i.replace('.','')
	i = i.replace('_VERB','')
	i = i.replace('_NOUN','')
	i = i.replace('_ADJ','')
	i = i.replace('_NUM','')
	i = i.replace('_ADP','')
	i = i.replace('_-','')
	i = i.replace('_X','')
	i = i.replace('_DET','')
	i = i.replace('_PRON','')
	i = i.replace('_','')
	i = i.replace('_PRT','')
	i = i.replace('CONJ','')


	val.append(i)

	j = len(i)
	leng.append(j)


df['word'] = val
df['word_length'] = leng

# print(df[:5])

# df.to_csv('C:/Users/benno/OneDrive/Python/NYCDSA/Final project/Datasets/a_cleaned.csv',index=False,columns=None)

print(df[:10])