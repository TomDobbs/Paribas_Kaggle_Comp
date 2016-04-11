import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as scs

class EDA(object):

    def __init__(self, data):
        self.data = data

    def overview(self):
        print '** Head of Data:\n'
        print self.data.head(5)
        print '\n\n** Data Description:\n'
        print self.data.describe()
        print '\n\n** Data Information:\n'
        print self.data.info()

    def correlations(self):
        #print self.data.cov()
        pass

    def plots(self):
        pass

    def classify_columns(self):
        pass

    def run(self):
        self.overview()
        self.correlations()
        self.plots()
        self.classify_columns()

# Drop NA_Rows
def not_applicable(df):
    total_na = 0
    null_columns = []
    n_rows = df.iloc[:,0].count()
    for col in df.columns:
        na_rows = df[col].isnull().sum()
        na_percentage = float(na_rows)/n_rows
        if na_percentage < .025 and na_rows != 0:
            print col, 'dropped', na_rows,'na rows @',\
                100 * round(na_percentage,3), "% nan's"
            total_na += na_rows
            df = df[df[col].notnull()]
            null_columns.append(col)

    print "Dropped", total_na, "Total NA Rows"

    return df, null_columns

def na_fill_str(df):
    str_fill_columns = []
    n_rows = df.iloc[:,0].count()
    for col in df.columns:
        na_rows = df[col].isnull().sum()
        na_percentage = float(na_rows)/n_rows
        if na_rows != 0:
            if df[col].dtype == 'object' or df[col].dtype == 'str':
                df[col] = df[col].fillna('Other')
                df[col] = df[col] + col
                print col, 'Other', na_rows,'na rows @', \
                    100 * round(na_percentage,3), "% nan's"
                str_fill_columns.append(col)

    return df, str_fill_columns

def na_fill_int(df):
    int_fill_columns = []
    n_rows = df.iloc[:,0].count()
    for col in df.columns:
        na_rows = df[col].isnull().sum()
        na_percentage = float(na_rows)/n_rows
        if na_rows != 0:
            if df[col].dtype == 'int64' or df[col].dtype == 'float64':
                mean = np.mean(df[col])
                df[col] = df[col].fillna(mean)
                print col, 'meaned', na_rows,'na rows @', \
                    100 * round(na_percentage,3), "% nan's"
                int_fill_columns.append(col)

    return df, int_fill_columns

# Create Dummy + Boolean Columns
def dummy(df):
    dummies = []
    bools = []
    for col in df.columns:
        n_variables = len(set(df[col]))
        if n_variables <= 150 and n_variables > 2:
            print col
            df[col] = df[col].apply(str_col)
            df[col] = df[col] + col
            variables = list(set(df[col]))
            df_dum = pd.get_dummies(df[col])
            df = pd.concat([df, df_dum], axis=1, join='inner')
            df = df.drop(variables[0], axis=1)
            df = df.drop(col, axis=1)
            dummies.append(col)
        if n_variables == 2:
            variables = list(set(df[col]))
            df[col] = 1 * (df[col] == variables[1])
            bools.append(col)

    return df, dummies, bools

def str_col(df_col):
    return str(df_col)

def corr_df(df, corr_val):
    '''
    Drops columns that are strongly correlated to other columns.
    This lowers model complexity, and aids in generalizing the model.
    Columns are dropped relative to the corr_val input (e.g. 0.8, 0.95)
    '''

    '''
    Creates Correlation Matrix and Instantiates
    '''
    corr_matrix = df.corr()
    iters = xrange(len(corr_matrix.columns) - 1)
    drop_cols = []
    '''
    Iterates through Correlation Matrix Table to find correlated columns
    '''
    for i in iters:
        for j in xrange(i):
            item = corr_matrix.iloc[j:(j+1), (i+1):(i+2)]
            col = item.columns
            row = item.index
            val = item.values
            if val > corr_val:
                print col.values[0], "|", row.values[0], "|", round(val[0][0],2)
                drop_cols.append(i)

    drops = sorted(set(drop_cols))[::-1]

    '''
    Drops the correlated columns
    '''
    for i in drops:
        col = df.iloc[:, (i+1):(i+2)].columns.values
        df = df.drop(col, axis=1)

    return df
