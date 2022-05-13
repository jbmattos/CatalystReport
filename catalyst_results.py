import pandas as pd

from data.datasets import load_data


class Results():
    def __init__(self, fund: int) -> None:
        self.__fund = fund
        self.__file_path = None
        self.__map_ch_db = {}
        
        self.__setup(fund)
        
    
    @property
    def assessments(self) -> pd.DataFrame:
        return self.__df[~self.__idx_filtered_out['default']]
    
    def __setup(self, file_path: str):
        data = self.load_data(file_path)
        
        
        
        return


    ##

    def get_validation():
        if 'validation' in dfs.keys():
            df_valid = dfs.pop('validation')
        elif 'Validation' in dfs.keys():
            df_valid = dfs.pop('Validation')
        else:
            df_valid = None
        return



if __name__ == "__main__":
    t = Assessments()
    t.load("vca_aggregated_7")
    print(t.get_full_assessments().shape)
    print("DONE")