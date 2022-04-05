#Showing data from CSV file, namely want to access the LAT and LONG coordinates
#Splitting geometry column into two seperate lat and long columns
import json
import pandas as pd
import numpy

class Data_Integration:


    def __init__(self):
        locations = ["new_general_household", "new_hospital", "new_miscs", "new_park",'new_school', 'new_senior_residence',
                    'new_store','new_workplace']
        # Needed for private repot
        tokens = ["GHSAT0AAAAAABHX6BUHP7GRP5Z7ZUCA4FBEYSMWB6Q", 'GHSAT0AAAAAABHX6BUH6BOSKCGRWISR3HPQYSMWENQ', 'GHSAT0AAAAAABHX6BUHCVDFHAGAN6CFHPOAYSMWFYA', 
                'GHSAT0AAAAAABHX6BUHZRLKXQH3MKCM3INIYSNJATQ', 'GHSAT0AAAAAABHX6BUGV3X6C3UZP6SU6XDIYSNJBKA', 'GHSAT0AAAAAABHX6BUHG6Z5E4D6WMBYX6NMYSNJBZA',
                'GHSAT0AAAAAABHX6BUGLCFMUOHUIPAPDSR6YSNJCSA', 'GHSAT0AAAAAABHX6BUHECIJSH2CQOAFKLHOYSNJC4A','GHSAT0AAAAAABHX6BUG7BJMN7PP4CMMTFJ4YSNJDMA' ]

        # Alternative (Smaller dataset)
        locations1 = [ "new_hospital", "new_miscs", "new_park", "new_school"]
        # Needed for private repot
        tokens1 = ['GHSAT0AAAAAABHX6BUGRF53GR6VOO6T6OMIYSNGZ7A', 'GHSAT0AAAAAABHX6BUHCVDFHAGAN6CFHPOAYSMWFYA', 'GHSAT0AAAAAABHX6BUHZRLKXQH3MKCM3INIYSNJATQ',
                    'GHSAT0AAAAAABHX6BUGV3X6C3UZP6SU6XDIYSNJBKA' ]

        self.locations = locations1
        self.tokens = tokens1
        self.dfs = self.read_multi_csv()
        self.minLongitude = self.get_range_long()[0]
        self.maxLongitude = self.get_range_long()[1]
        self.minLatitude = self.get_range_lat()[0]
        self.maxLatitude = self.get_range_lat()[1]


    def read_multi_csv(self): 
        dfs = [] # store multiple datafames
        if len(self.locations) == 1:
            print('hi')
            file = 'https://raw.githubusercontent.com/covid-map-ingestion/tree/main/update_kingston_data/after_sorting/split_version/'+str(locations[0])+'.csv'+'?token='+tokens[0]
            df = pd.read_csv(file)
            dfs.append(df)
        else: 
            for x, y in zip(self.locations, self.tokens):         
                file = 'https://raw.githubusercontent.com/QuMuLab/covid-map-ingestion/main/update_kingston_data/after_sorting/split_version/'+str(x)+'.csv'+'?token='+y  
                            
                #print(file)         
                df = pd.read_csv(file)       
                dfs.append(df)
                #df = []
                #dfs.append(df)
            
            return dfs


    #all_dfs = read_multi_csv(locations, tokens) 
    # Single Data Frame test
    #file = ['new_general_household']
    #token = ['GHSAT0AAAAAABHX6BUHP7GRP5Z7ZUCA4FBEYSMWB6Q']
    #df = pd.read_csv('https://raw.githubusercontent.com/QuMuLab/covid-map-ingestion/tree/main/update_kingston_data/after_sorting/split_version/new_hospital.csv?token=GHSAT0AAAAAABHX6BUH6BOSKCGRWISR3HPQYSMWENQ')
    #dfs = read_multi_csv(locations1, tokens1)


    # Normalize Dataset
    def normalize(self):
        arr = []
        '''
        for df in self.dfs:
            df_max_scaled = df.copy()
            df_max_scaled['Latitude'] = df_max_scaled['Latitude'] /df_max_scaled['Latitude'].abs().max()
            df_max_scaled['Longitude'] = df_max_scaled['Longitude'] /df_max_scaled['Longitude'].abs().max() 
            arr.append(df_max_scaled)

        '''
        return self.dfs

    def get_range_long(self):
        globalMinLong = float('inf')
        globalMaxLong = float('-inf')

        for x in self.dfs:
            globalMinLong = min( x['Longitude'].min(), globalMinLong)
            globalMaxLong = max( x['Longitude'].max(), globalMaxLong)

        return globalMinLong,  globalMaxLong

    def get_range_lat(self):
        globalMinLat = float('inf')
        globalMaxLat = float('-inf')

        for x in self.dfs:
            globalMinLat = min( x['Latitude'].min(), globalMinLat)
            globalMaxLat = max( x['Latitude'].max(), globalMaxLat)

        return globalMinLat, globalMaxLat



    def get_hospitals(self):
        normalized = self.normalize()
        hospitals = normalized[0][["Latitude", "Longitude"]].to_numpy()
        return hospitals

    def get_misc(self):
        normalized = self.normalize()
        misc = normalized[1][["Latitude", "Longitude"]].to_numpy()
        return misc

    def get_parks(self):
        normalized = self.normalize()
        parks = normalized[2][["Latitude", "Longitude"]].to_numpy()
        return parks
    
    def get_schools(self):
        normalized = self.normalize()
        schools = normalized[3][["Latitude", "Longitude"]].to_numpy()
        return schools


integrated = Data_Integration()
print(integrated.get_schools())
print(integrated.get_parks())

#print(integrated.dfs)





