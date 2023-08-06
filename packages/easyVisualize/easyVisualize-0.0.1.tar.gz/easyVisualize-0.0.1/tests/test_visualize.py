from unicodedata import numeric
from easyVisualize import visualize
import pandas as pd

import easyVisualize.visualize as a
import pandas as pd

train_df=pd.read_csv("C:/Users/Tolga/Desktop/WorkSpace/easyVisualize/tests/veriler.csv", sep="," )
train_df.head()
cat_val=a.categorical(train_df)
a.numerical(train_df)
a.splits(train_df, 10,"yas")
X_train=a.X_train
X_train
a.prob_his(train_df,"yas","boy")
a.scatter_p(train_df,"yas","kilo")
  