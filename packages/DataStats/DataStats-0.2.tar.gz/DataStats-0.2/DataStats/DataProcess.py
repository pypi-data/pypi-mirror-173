from statsbombpy import sb
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
pd.options.display.max_columns= None

class StatsObtention:
    
    def __init__(self, c_name=str, c_gender=str, s_name=str):
        self.c_name= c_name
        self.c_gender= c_gender
        self.s_name= s_name
        self.df= sb.competitions()
        self.competition= self.df['competition_name'].unique()
        
        if self.c_name in self.competition:
            self.df= self.df[self.df['competition_name']== self.c_name]
            self.gender= self.df['competition_gender'].unique()
        else:
            print(f'Wrong introduced data, the posible values for competition_name are {self.competition}')
            
        if self.c_gender in self.gender:
            self.df= self.df[self.df['competition_gender']== self.c_gender]
            self.season= self.df['season_name'].unique()
        else:
            print(f'Wrong introduced data, the posible values for competition_gender are {self.gender}')
        
        if self.s_name in self.season:
            self.df= self.df[self.df['season_name']== self.s_name]
        else:
            print(f'Wrong introduced data, the posible values for season_name are {self.season}')
        
        self.match= sb.matches(competition_id= self.df['competition_id'].values[0], season_id= self.df['season_id'].values[0])
        self.matches_id= self.match['match_id'].values
        
    def selection(self):
        return self.df
    
    def matches(self):
        return self.match
    
    def events(self):
        print('This proccess may take some time')
        self.results= dict()
        self.tables = dict()
        
        for i in range(len(self.matches_id)):
            print(round((i/len(self.matches_id)*100),1),'%')
            self.results[self.matches_id[i]]= sb.events(match_id= self.matches_id[i], split= True, flatten_attrs= False)        
        
        for e in self.results[self.matches_id[0]].keys():
            self.df = pd.DataFrame()
            print(f'Creating the united table {e} of all parties')
            for i in self.results.keys():
                try:
                    self.df = pd.concat([self.df, self.results[i][e]])
                except:
                    pass
            self.tables[e] = self.df
        print('Process completed')
        
        return [self.results, self.tables]