import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import ast
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
import warnings;
import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['C:\\Users\\win-10\\PycharmProject\\chatbot', 'C:/Users/win-10/PycharmProject/chatbot'])

warnings.simplefilter('ignore')
apps = pd.read_csv('./input_path/apps.tsv', delimiter='\t',encoding='utf-8')
user_history = pd.read_csv('./input_path/user_history.tsv', delimiter='\t',encoding='utf-8')
jobs = pd.read_csv('./input_path/jobs.tsv', delimiter='\t',encoding='utf-8', error_bad_lines=False)
users = pd.read_csv('./input_path/users.tsv' ,delimiter='\t',encoding='utf-8')
test_users = pd.read_csv('./input_path/test_users.tsv', delimiter='\t',encoding='utf-8')
apps.head()
apps.shape
apps.info()
user_history.head()

