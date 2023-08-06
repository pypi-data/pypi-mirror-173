"""
28.10.2022 
Tolga TANRISEVER
this package prepared for basic EDA operations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px 
from sklearn.impute import SimpleImputer
from collections import Counter
from sklearn.model_selection import  StratifiedKFold, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


""" Main
    categorical 
    input :a pandas dataframe
    output :categorical variable for data frame  
"""
def categorical(train_df):
    cols=train_df.columns
    num_cols = train_df._get_numeric_data().columns
    cols=train_df.columns
    cat_col=list(set(cols) - set(num_cols)) 
    return cat_col

 
""" Main
    numerical
    input :a pandas dataframe
    output :numerical variable for data frame
"""
def numerical(train_df):
    num_cols = train_df._get_numeric_data().columns
    return num_cols

""" Main
    mis_values
    input train_df["var"] 
    output  train_df["var"].mean() from imputer 
    use :
        "mis_Value(train_df["yas"])
        train_df=train_df.fillna(mis_Value(train_df["yas"]))"
"""
def mis_Value(train_df:pd.DataFrame):
    imputer = SimpleImputer(missing_values=np.nan,strategy='mean')
    val=train_df.values
    imputer=imputer.fit(val.reshape(-1,1))
    val=imputer.transform(val.reshape(-1,1))
    return val.mean()


""" Main
    numerical
    input :a pandas dataframe and dataframe's variables
    output :outliers
    "train_df.loc[detect_outliers(train_df,numerical(train_df))]
    train_df = train_df.drop(detect_outliers(train_df,["b","a","c"]),axis = 0).reset_index(drop = True)"
"""
def detect_outliers(df,features):
    outlier_indices = []
    
    for c in features:
        # 1st quartile
        Q1 = np.percentile(df[c],25)
        # 3rd quartile
        Q3 = np.percentile(df[c],75)
        # IQR
        IQR = Q3 - Q1
        # Outlier step
        outlier_step = IQR * 1.5
        # detect outlier and their indeces
        outlier_list_col = df[(df[c] < Q1 - outlier_step) | (df[c] > Q3 + outlier_step)].index
        # store indeces
        outlier_indices.extend(outlier_list_col)
    
    outlier_indices = Counter(outlier_indices)
    multiple_outliers = list(i for i, v in outlier_indices.items() if v > 2)
    
    return multiple_outliers

""" Main
    numerical
    input :a pandas dataframe and for histogram x and y axis 
    output :basic hist and bar plots
"""

def prob_his(train_df,variable_x,variable_y):
    fig = px.histogram(train_df,x=variable_x,marginal='box',title=variable_x, width=700, height=500,color_discrete_sequence=['indianred'])
    fig.update_layout(bargap=0.1)
    fig.show()
    fig = px.histogram(train_df,x = variable_x, y = variable_y,color=variable_x,histfunc='avg',marginal='box',barmode='overlay',title=variable_x, width=700, height=500)
    fig.update_layout(bargap=0.1,barmode='stack')
    fig.show()
    fig1 = px.box(train_df, x=variable_x, y=variable_y,color=variable_x,width=700,height=500,)
    fig1.update_traces(quartilemethod="exclusive")
    fig1.show()

""" Main
    numerical
    input :a pandas dataframe and for histogram x and y axis 
    output :scatter plots
"""

def scatter_p(train_df,variable_x,variable_y):
    fig = px.scatter(train_df,x=variable_x,y=variable_y,title=variable_x,width=700,height=500,marginal_x="histogram", marginal_y="rug",trendline="ols",color=variable_x)
    fig.show()

""" Main
    numerical
    input :a pandas dataframe 
    output :heatmap
"""
def heatmap(train_df):
    sns.heatmap(train_df.corr(), annot = True,annot_kws={'size': 10}, fmt = ".2f")
    plt.show()

""" Main
    numerical "if he concat train and test "
    input :a pandas dataframe and train df len and droplabels
    output :scatter plots
"""

def splits(train_df,train_df_len,droplabels):
    global X_train,X_test,y_train,y_test
    
    train=train_df[:train_df_len]
    X_t=train.drop(labels=droplabels,axis=1)
    y_t=train[droplabels]
    X_tr,X_te,y_tr,y_te=train_test_split(X_t,y_t,test_size=0.35,random_state=42)
    print("Now you can use the following variables")
    print("X_train",len(X_t))
    print("X_test",len(X_t))
    print("y_train",len(y_t))
    print("y_test",len(y_t))
    X_train=X_tr.copy()
    X_test=X_te.copy()
    y_train=y_tr.copy()
    y_test=y_te.copy()