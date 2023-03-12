import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from exceptions.exception import TableNotFound, URLReturnedInvalidResponse


class TableScraper:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def get_table_names(self) -> list:
        table_names = []
        for table in self.soup.find_all('table'):
            if table.get('class') is not None:
                table_names.append(" ".join(table.get("class")))
        return table_names

    def get_table_counts(self) -> int:
        table_names = []
        for table in self.soup.find_all('table'):
            if table.get('class') is not None:
                table_names.append(" ".join(table.get("class")))
        return len(table_names)

    def __write_df_to_file(self, df: pd.DataFrame, file_type: str, i: int):
        if not os.path.exists('output'):
            os.makedirs('output')
        if file_type == 'excel':
            return df.to_excel(f'output/table_{i}.xlsx')
        else:
            return df.to_csv('output/')

    def get_all_tables_data(self, persist=False, file_type='excel') -> list[pd.DataFrame]:
        """
               :param persist: True if you want to save the data. false otherwise
               :param file_type: Format in which data needs to be saved
               :return: List of Dataframes where each dataframe corresponds to one table, None otherwise

        """
        tables = soup.find_all("table")
        dfs = []
        i = 0
        for table in tables:
            headers = [th.text for th in table.find_all("th")]
            data = []
            try:
                for tr in table.find_all("tr"):
                    row = []
                    for td in tr.find_all("td"):
                        row.append(td.text)
                    data.append(row)

                df = pd.DataFrame(data, columns=headers)
                if persist:
                    try:
                        i += 1
                        self.__write_df_to_file(df, file_type, i)
                    except Exception as e:
                        print(f'Exception occurred while saving data : {e}')

                dfs.append(df)
            except ValueError as e:
                print(f'Warning - Unparsable table {" ".join(table.get("class"))} - Skipping')
                continue
        return dfs

    def get_dataframe_by_table_class(self, table_name, persist=False, file_type='excel') -> pd.DataFrame:
        """
        :param table_name: The teable name for which you want to extract data
        :param persist: True if you want to save the data. false otherwise
        :param file_type: Format in which data needs to be saved
        :return: Dataframe if table data is parsable, None otherwise
        """
        i = 0
        table = self.soup.find('table', class_=table_name)
        if table is None:
            raise TableNotFound(f'Table {table_name} not found in soup object')
        headers = [th.text for th in table.find_all("th")]
        data = []
        try:
            for tr in table.find_all("tr"):
                row = []
                for td in tr.find_all("td"):
                    row.append(td.text)
                data.append(row)

            df = pd.DataFrame(data, columns=headers)
            if persist:
                try:
                    i += 1
                    self.__write_df_to_file(df, file_type, i)
                except Exception as e:
                    print(f'Exception occurred while saving data : {e}')
        except ValueError as e:
            print(f'Warning - Unparsable table {" ".join(table.get("class"))} - Skipping')
            return None
        return df

    def get_csv_from_df(self, dataframe):
        try:
            dataframe.to_csv('tournament.csv')
        except Exception as e:
            print(f"Some exception occurred {str(e)}")


def get_soup_from_url(url):
    """
    Helper function that takes a URL and returns a soup object that can be used with TableScraper class
    :param url: The URL for which soup object needs to be generated
    :return: soup
    """
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    header = {'User-Agent': user_agent}
    session = requests.session()
    session.headers = header
    req = session.get(url)
    if req.status_code != 200:
        raise URLReturnedInvalidResponse(f'URL returned invalid response code {req.status_code}')
    session.close()
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup


'''
Below are example usages of the TableScraper class
'''
soup = get_soup_from_url('https://liquipedia.net/valorant/Portal:Statistics')
tab = TableScraper(soup)
table_names = tab.get_table_names()
table_count = tab.get_table_counts()
tables = tab.get_all_tables_data(persist=True)
