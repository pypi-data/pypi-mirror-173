def lab1():
    pass
    return '''import csv
import pandas as pd
from sklearn import preprocessing from
sklearn import tree
#Reading the values from csv file
print("Reading the Values from CSV File")
print('-'*50) data=pd.read_csv('Marks.csv',sep=',')
print(data)
print()
-------------------------------------------
#Removing the Specified Attribute
print("Removing Specified Attribute")
print('-'*50)
with open("Marks.csv", "r") as source:
reader = csv.reader(source)
with open("Marks1.csv", "w") as result:
writer = csv.writer(result)
for c in reader:
# Use CSV Index to remove a column from CSV
#c[4] = c['marks5']
writer.writerow((c[0], c[1],
c[2],c[3]))
data1=pd.read_csv('Marks1.csv',sep=',')
print(data1)
print()
#Standardization of Data
#To standardize a dataset means to scale all of
the values in the dataset
#such that the mean value is 0 and the standard
deviation is 1.
#We use the following formula to standardize
the values in a dataset: #xnew = (xi – x) / s
#where: xi: The ith value in the dataset,x: The
sample mean, s: The sample standard deviation
print("Standardization of Data") print('-
'*50)
data2=pd.read_csv('Marks1.csv',sep=',')
standardizedData = (data2-
data2.mean())/data2.std() print(standardizedData)
print()
------------------------------------------
#Normalization of Data
print("Normalization of Data")
print('-'*50)
data3=pd.read_csv('Marks1.csv',sep=',') scaler
= preprocessing.MinMaxScaler(feature_ran
ge=(85,99))
marks = data3.columns
d = scaler.fit_transform(data3)
scaledData = pd.DataFrame(d,
columns=marks)
normalizedData=scaledData.head()
print(normalizedData)
print()
-------------------------------------------
#Discrimination of a continous valued attribute
print("Discrimination of a continous valued
attribute")
print('-'*50)
data4=pd.read_csv('Marks1.csv',sep=',')
x=data4.iloc[:,:-1].values #till second last
column of the data frame
y=data4.iloc[:,-1].values #last column of data
frame
clf = tree.DecisionTreeClassifier() clf =
clf.fit(x, y) print(tree.plot_tree(clf))
'''

def lab2():
    pass
    return '''pip install apyori
-------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
df = pd.read_csv('dataset1.csv')
df.head()
df = pd.read_csv('dataset1.csv', header=None)
df.head()
df.fillna(0,inplace=True)
df.head()
df.shape
#for using aprori need to convert data in list format..
# transaction =
[['apple','almonds'],['apple'],['banana','apple']]....
transactions = []
for i in range(0,len(df)):
transactions.append([str(df.values[i,j])
for j in range(0,2)
if str(df.values[i,j])!='0'])
transactions[1]
rules=apriori(transactions,min_support=0.003,min_
confidance=0.2,min_lift=3,min_length=2)
Results = list(rules)
Results
#convert result in a dataframe for further
operation...
df_results = pd.DataFrame(Results)
df_results.head()'''

def lab3():
    pass
    return '''import pandas as pd
data = pd.read_csv('drive/My Drive/Colab Noteboo
ks/208W5A0508/Lab - 3/golf.csv')
print(data)
from sklearn.preprocessing
import OneHotEncoder
oe = OneHotEncoder(sparse=False)
df = oe.fit_transform(data)
print(df)
resultant decision tree.
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier,
plot_tree
y = data['Golf Play']
X_train, X_test, y_train, y_test = train_test_split(df,
y, random_state=10, test_size=0.3)
clf = DecisionTreeClassifier(criterion='entropy')
clf.fit(X_train,y_train)
plot_tree(clf,filled=True)
plt.show()
'''

def lab4():
    return '''import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:, [3, 4]].values
from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11):
kmeans = KMeans(n_clusters = i, init = 'kmeans++', random_state = 42)
kmeans.fit(X)
wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
kmeans = KMeans(n_clusters = 5, init = 'kmeans++', random_state = 42)
y_kmeans = kmeans.fit_predict(X)
plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0,
1], s = 100, c = 'red', label = 'Cluster 1')
plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1,
1], s = 100, c = 'blue', label = 'Cluster 2')
plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2,
1], s = 100, c = 'green', label = 'Cluster 3')
plt.scatter(X[y_kmeans == 3, 0], X[y_kmeans == 3,
1], s = 100, c = 'cyan', label = 'Cluster 4')
plt.scatter(X[y_kmeans == 4, 0], X[y_kmeans == 4,
1], s = 100, c = 'magenta', label = 'Cluster 5')
plt.scatter(kmeans.cluster_centers_[:, 0],
kmeans.cluster_centers_[:, 1], s = 300, c = 'yellow',
label = 'Centroids')
plt.title('Clusters of customers')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()'''

def lab5():
    return '''import pandas as pd from pandas import datetime
import matplotlib.pyplot as plt
def parser(x):
return datetime.strptime(x,'%Y-%m')
sales = pd.read_csv('/content/drive/My Drive/Data
Analytics lab work/198W1 A0586/Lab
5/shampoo.csv',index_col= 0, parse_dates=[0]
,date_parser=parser)
sales.head() -- sales.plot() ---
from statsmodels.graphics.tsaplots imp ort plot_acf
plot_acf(sales) --- sales.shift(1) -- - sales_diff=
sales.diff(periods=1) sales_diff = sales_diff[1:]
sales_diff.head() --- plot_acf(sales_diff) -- -
sales_diff.plot() --- X = sales.values train = X[0:27]
test = X[26:] predictions = []
train.size --- test.size ---
#Autoregressive model from
statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squa red_error
model_ar = AR(train)
model_ar_fit = model_ar.fit() predictions =
model_ar_fit.predict(start =26,end=36)
test --- plt.plot(test)
plt.plot(predictions,color='red')--- sales.plot() ---
#ARIMA
from statsmodels.tsa.arima_model imp ort ARIMA
model_arima = ARIMA(train,order=(9, 2, 0))
model_arima_fit = model_arima.fit()
print(model_arima_fit.aic)
predictions= model_arima_fit.forecast( steps=10)[0]
predictions ---
plt.plot(test)
plt.plot(predictions,color='red')---
mean_squared_error(test,predicti ons)---
import itertools p=d=q=range(0,5) pdq =
list(itertools.product(p,d,q)) pdq –
import warnings warnings.filterwarnings('ignore') for
param in pdq:
try:
model_arima = ARIMA(train,orde r=param)
model_arima_fit = model_arima.fit()
print(param,model_arima_fit.aic)
except: continuee'''

def lab6():
    return '''import numpy as np # linear algebra
import pandas as pd # data processing, CSV file
train =
pd.read_csv('/content/drive/MyDrive/Dalab/Train.c
sv')
test =
pd.read_csv('/content/drive/MyDrive/Dalab/Test.csv')
train.head()
#Counting the number of words in each review
def num_of_words(df):
df['word_count'] = df['text'].apply(lambda x :
len(str(x).split(" ")))
print(df[['text','word_count']].head())
num_of_words(train)
num_of_words(test)
#Counting and Removing the Stop Words
import nltk
#the below command use it once and download the
packages
nltk.download()
# a window will open in the select popular under
collections
from nltk.corpus import stopwords
stop = stopwords.words('english')
def stop_words(df):
df['stopwords'] = df['text'].apply(lambda x: len([x
for x in x.split() if x in stop]))
print(df[['text','stopwords']].head())
stop_words(train)
stop_words(test)
def stop_words_removal(df):
df['text'] = df['text'].apply(lambda x: " ".join(x for x
in x.split() if x not in stop))
stop_words_removal(train)
stop_words_removal(test)
#Converting text to lowercase letterdef
lower_case(df):
df['text'] = df['text'].apply(lambda x: "
".join(x.lower() for x in x.split()))
print(df['text'].head())
lower_case(train) lower_case(test)
#Removing special Characters and Punctuation
def punctuation_removal(df):
df['text'] = df['text'].str.replace('[^\w\s]','')
print(df['text'].head())
punctuation_removal(train)
punctuation_removal(test)
#Remove the most frequently used words and less
frequently used words
freq = pd.Series('
'.join(train['text']).split()).value_counts()[:10]
freq
freq = list(freq.index)
def frequent_words_removal(df):
df['text'] = df['text'].apply(lambda x: " ".join(x for x
in x.split() if x not in freq))
print(df['text'].head())
frequent_words_removal(train
)
frequent_words_removal(test)
freq = pd.Series('
'.join(train['text']).split()).value_counts()[-10:]
freq
freq = list(freq.index)
def rare_words_removal(df):
df['text'] = df['text'].apply(lambda x: " ".join(x for
xin x.split() if x not in freq))
print(df['text'].head())
rare_words_removal(train)
rare_words_removal(test)
from textblob import
TextBlobdef
spell_correction(df):
return df['text'][:5].apply(lambda
x:str(TextBlob(x).correct()))
spell_correction(train)
spell_correction(test)
#Tokenizing
def
tokens(df):
return
TextBlob(df['text'][1]).words
tokens(train)
tokens(test
)
#Stemmin
g
from nltk.stem import
PorterStemmerst = PorterStemmer()
def stemming(df):
return df['text'][:5].apply(lambda x: "
".join([st.stem(word) for word in
x.split()]))stemming(train)
stemming(test)
#Applying Term Frequency – Inverse
DocumentFrequency (TF-IDF
tf1 = (train['text'][1:2]).apply(lambda x:
pd.value_counts(x.split(" "))).sum(axis
=0).reset_index()
tf1.columns = ['words','tf']
for i,word in
enumerate(tf1['words']):tf1.loc[i,
'idf'] =
np.log(train.shape[0]/(len(train[train['text'].str.conta
ins(word)])))
tf1['tfidf'] = tf1['tf'] * tf1['idf']
tf1
#Sentiment Analysis
def polarity_subjectivity(df):
return df['text'][:5].apply(lambda x:
TextBlob(x).sentiment)
polarity_subjectivity(train)
polarity_subjectivity(test)
def sentiment_analysis(df):
df['sentiment'] = df['text'].apply(lambda x:
TextBlob(x).sentiment[0] )
return df[['text','sentiment']].head()
sentiment_analysis(train)
sentiment_analysis(test)'''

