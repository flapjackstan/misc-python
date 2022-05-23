import pandas as pd
import numpy as np

def main():
    try:
        #Path to csv
        csv_path = 'path goes here'

        # Columns from csv to grab
        usecols = ['col1','col2','col3','col4']

        # Columns to randomize
        permute = ['col2', 'col3']

        #Columns that remain the same (col 1 and 4)
        non_permute = list(set(usecols) - set(permute))


        dataframe = pd.read_csv(csv_path,
                                    usecols=usecols,
                                    low_memory=False) # set true if really large csv

        # Create copy of dataframe with columns that are to remain the same
        dataframe_random = dataframe[non_permute].copy(deep=True)

        # Recreating and index
        dataframe_random = dataframe.reset_index()
        dataframe_random = dataframe_random.rename(columns={'index':'ID'})

        # Setting cols to ramdomized cols based of original data
        for col in permute:
            dataframe_random[col] = np.random.permutation(dataframe[col].values)

        dataframe_random.to_csv('random_data.csv')
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
          
        error_type = str(exc_type)
        line = exc_tb.tb_lineno
        word =  error_type + ' at Line '
        error = word+str(line)

        message = (error + ': ' + str(e))
        
        print(message)

if __name__ == '__main__':
    main()