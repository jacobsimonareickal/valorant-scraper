import requests
from bs4 import BeautifulSoup
import pandas as pd

from exceptions.exception import TableNotFound


class ValorantScraper():
    def __init__(self, soup: BeautifulSoup, table_name: str):
        self.soup = soup
        self.column_names = ['Player',
                             'Maps',
                             'K',
                             'D',
                             'A',
                             'KD',
                             'KDA',
                             'ACS/Map',
                             'K/Map',
                             'D/Map',
                             'A/Map']
        self.table_name = table_name
        self.tournament_df = pd.DataFrame()

    def get_tournament_data(self) -> pd.DataFrame:
        table_data = self.soup.find('table', class_=self.table_name)
        if table_data is None:
            raise TableNotFound(f'Table not found {table_data} in soup object')
        for row in table_data.tbody.find_all('tr'):
            columns = row.find_all('td')
            if columns != []:
                Player = columns[0].text.strip()
                Maps = columns[3].text.strip()
                K = columns[4].text.strip()
                D = columns[5].text.strip()
                A = columns[0].text.strip()
                KD = columns[0].text.strip()
                ACS_Map = columns[0].text.strip()
                K_Map = columns[0].text.strip()
                D_Map = columns[0].text.strip()
                A_Map = columns[0].text.strip()
                self.tournament_df = self.tournament_df.append({'Player': Player, 'Maps': Maps, 'K': K, 'D': D,
                                                                'A': A, 'KD': KD, 'ACS_Map': ACS_Map, 'K_Map': K_Map,
                                                                'D_Map': D_Map, 'A_Map': A_Map},
                                                               ignore_index=True)
        return self.tournament_df

    def get_csv_from_df(self, dataframe):
        try:
            dataframe.to_csv('tournament.csv')
        except Exception as e:
            print(f"Some exception occurred {str(e)}")


# req = requests.get('https://liquipedia.net/valorant/CECC_Regionals/West/Statistics')
req = requests.get('https://liquipedia.net/valorant/VCT/2023/LOCK_IN_S%C3%A3o_Paulo/Statistics')
soup = BeautifulSoup(req.content, 'html.parser')
val = ValorantScraper(soup, 'wikitable-striped')
tournament_dataframe = val.get_tournament_data()
val.get_csv_from_df(tournament_dataframe)


print('hello')
