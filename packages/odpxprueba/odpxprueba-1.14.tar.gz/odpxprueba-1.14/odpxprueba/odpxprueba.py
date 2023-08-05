
import pandas
import numpy
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

"""

Outliers detection  package.
It is a package generated to perform easy outlier detection for both dataframes and arrays. 
It incorporates the use of graphics for a better understanding of these.

"""

class odpxprueba:

    def __init__(self, df, col = 'all', method = 'all'):
        self.df = df
        self.col = col
        self.method = method
    
    """ The class do not requiere any argument """

    def __outliers_iqr(self, df, col):

        """ With this private function we can detect outliers using the IQR method. """

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        return list(df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)].index)

    def __outliers_zscore(self, df, col):

        """ With this private function we can detect outliers using the zscore method. """

        z = numpy.abs(stats.zscore(df[col]))
        return list(df[(z > 3) | (z < -3)].index) 

    def __stripplot(self, df, col, palette):

        """ A private function to make a plot of one numeric feature where outliers are indicated """
        
        title = col[0].capitalize()
        sns.stripplot(data=df, y=col[0], hue="outliers", palette=palette, size = df['size'])
        plt.xlabel('Observations', fontsize=14, fontweight='bold'), plt.ylabel(title, fontsize=14, fontweight='bold'), plt.title(f'{title} distribution', fontsize=16, fontweight='bold');
        plt.grid(True, alpha=0.3, linestyle='--', color='black', axis='y')
        plt.show();

    def __dataframe_plot(self, df, col, outliers, size):

        """ A private function to create the dataframe necesary to use the __stripplot function """

        colname, outliers_tag, size = list(df[col[0]]), ['normal' if _ not in outliers[col[0]] else 'outlier' for _ in range(len(df))], [size[0] if _ not in outliers[col[0]] else size[1] for _ in range(len(df))]
        new_df = pandas.DataFrame([colname, outliers_tag, size]).T.rename(columns={0: col[0], 1: 'outliers', 2: 'size'})
        new_df['size'] = new_df['size'].astype(int)
        return new_df

    ########################################################################################################################################################################################################################

    def outliers(self):

        """ 
        
        This is one of the main function that requieres the 3 main arguments: df, col and method.
        
        df: Could be a dataframe, list or an array.
        col: The column to detect outliers. It can be a list or a string in case it is only one column. "all" is also a valid option to select every numeric column of the dataset (default = 'all').
        method: The method to detect outliers. It can be "iqr", "zscore" or "all". "all" is the default option (default = 'all').
        
        """

        if type(self.df) != pandas.core.frame.DataFrame:
            try: 
                self.df = pandas.DataFrame(self.df)
                self.df.columns = [str(x) for x in self.df.columns]
                for column in self.df.columns:
                    try: self.df[column] = pandas.to_numeric(self.df[column])
                    except: pass
            except: raise ValueError('The data must be a DataFrame, list or a numpy array')
        else: pass

        numeric_columns = self.df.select_dtypes(include=numpy.number).columns
        if self.col == 'all': self.col = numeric_columns
        elif type(self.col) != list: self.col = [self.col]
        else: raise ValueError('Use list, an string or use "all" argument to select all columns')


        if set(self.col).issubset(numeric_columns):
            
            if self.method == 'iqr': return {v: self.__outliers_iqr(self.df, v) for v in self.col}
            elif self.method == 'zscore': return {v: self.__outliers_zscore(self.df, v) for v in self.col}
            elif self.method == 'all':
                outliers_iqr, outliers_zscore =  [self.__outliers_iqr(self.df, v) for v in self.col], [self.__outliers_zscore(self.df, v) for v in self.col]
                return {v: list(set(outliers_iqr[i] + outliers_zscore[i])) for i, v in enumerate(self.col)}

            else: raise ValueError('Method must be iqr, zscore or all')

        else: raise ValueError('Columns must be numeric')

    ########################################################################################################################################################################################################################

    def plot_outliers(self, col, size = [5, 7], palette = ((133/255, 202/255, 194/255), (38/255, 70/255, 83/255)) ):

        """

        This function is used to plot the outliers detected. It requieres the same arguments as the outliers function.
        However, it includes 2 extra arguments to custome the striplot

        df: Could be a dataframe, list or an array.
        col: The column to detect outliers. It just can be 1 numeric column in string or list format.
        method: The method to detect outliers. It can be "iqr", "zscore" or "all". "all" is the default option (default = 'all').
        size: A list with the size of the points. The first value is for the normal points and the second for the outliers (default = [5, 7]).
        palette: A tuple with the colors to use in the plot. The first value is for the normal points and the second for the outliers (default = ((133/255, 202/255, 194/255), (38/255, 70/255, 83/255))).

        """
        if self.df[col].isnull().sum() > 0:
            df = self.df.copy()
            df.dropna(subset=[col], inplace=True)
            print(f"The selected column has null values. {df.shape[0] - self.df.shape[0]} rows were removed in order to plot the data.")
        else: df = self.df.copy()

        if type(df) != pandas.core.frame.DataFrame:
            try: 
                df = pandas.DataFrame(df)
                df.columns = [str(x) for x in df.columns]
                for column in df.columns:
                    try: df[column] = pandas.to_numeric(df[column])
                    except: pass
            except: raise ValueError('The data must be a DataFrame, list or an array')
        else: pass

        numeric_columns = df.select_dtypes(include=numpy.number).columns
        if type(col) != list: col = [col]
        else: pass

        if (set(col).issubset(numeric_columns)):
            if len(col) == 1:

                if self.method == 'iqr':  
                    outliers = {v: self.__outliers_iqr(df, v) for v in col}
                    new_df = self.__dataframe_plot(df, col, outliers, size)
                    self.__stripplot(new_df, col, palette)

                elif self.method == 'zscore': 
                    outliers = {v: self.__outliers_zscore(df, v) for v in col}
                    new_df = self.__dataframe_plot(df, col, outliers, size)
                    self.__stripplot(new_df, col, palette)            
                    
                elif self.method == 'all':
                    outliers_iqr, outliers_zscore =  [self.__outliers_iqr(df, v) for v in col], [self.__outliers_zscore(df, v) for v in col]
                    outliers = {v: list(set(outliers_iqr[i] + outliers_zscore[i])) for i, v in enumerate(col)}
                    new_df = self.__dataframe_plot(df, col, outliers, size)
                    self.__stripplot(new_df, col, palette)

                else: raise ValueError('Method must be iqr, zscore or all')

            else: raise ValueError('Use only one numeric column')
        else: raise ValueError('The column may not exist or may not be numeric')