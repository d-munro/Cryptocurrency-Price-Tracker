# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 16:30:22 2022

Powered by CoinGecko API

@author: Dylan Munro
"""

from typing import Final
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import datetime
import pandas as pd

class AssetManager:
    """
    Class responsible for driving back-end program execution
    
    (Long Description TODO)
    
    Attributes:
        tickers_to_assets (dict[string:Asset]): 
            Dictionary mapping the ticker of an asset to its object representation
        names_to_tickers (dict[string:string]): 
            Dictionary mapping the name of an asset to its ticker
        assets_to_graphs (dict[Asset:Graph]): 
            Dictionary mapping each Asset with its current graphical representation
            
    Methods:
        
    """
    
    _REQUIRED_COLUMNS:Final = {"ticker", "date", "time", "price"}
    
    def __init__(self, data):
        if (data is not None):
            self._check_column_validity(data)
            self._generate_assets(data)
    
    def _check_column_validity(self, data):
        required_columns_remaining = self._REQUIRED_COLUMNS
        for column in data.columns:
            if column.lower() in self._REQUIRED_COLUMNS:
                required_columns_remaining.remove(column.lower())
        if len(required_columns_remaining) > 0:
            raise ValueError("The spreadsheet is missing several required columns")
    
    def _contains_duplicate_columns(self, column_names):
        parsed_names = set()
        for column in column_names:
            if column in parsed_names:
                return True
            parsed_names.add(column)
        return False
    
    def _generate_assets(self, data):
        pass

"""
Contains all information about an asset

class variables:
    name - The full name of the asset (Ex: Apple, Bitcoin)
    ticker - The ticker for the asset (Ex: AAPL, BTC)
    type - Declares if a ticker is for a cryptocurrency or a stock
    
"""
class Asset:
    
    def __init__(self, *args):
        pass
    
    """
    Returns the price of the asset at a specified date
    """
    #def get_price(self, date: datetime.datetime()) -> float:
     #   pass
    
#get_price(ticker, datetime.datetime(year, month, day, hour, minute, second))

"""
Contains all methods for plotting graphs of the specified ticker
    
"""
class Graph:
    
    """
    params:
        asset: the Asset object containing all relevant information for the graph
    """
    def __init__(self, asset: Asset):
        pass
        
    """
    Plots the last 50 days of the closing price for the specified asset
    """
    def plot_asset(self, final_date=datetime.date.today()):
        pass

"""
Handles all IO requests from the user

class variables:
    file - The file which stores asset data if not using coingecko API
"""
class IO:
    
    #Final means static class checkers wont reassign. Must import Final from typing
    _SUPPORTED_FILES:Final = {".csv", ".xlsx"}
    
    def __init__(self):
        self._manager = None
        
    def get_file_extension(self, file_path):
        """
        
        raises:
            ValueError: If the file being loaded is not supported
        """
        file_extension = ""
        extension_index = len(file_path)
        extension_found = False
        
        #Start at end of file_path because extension is at end of file name
        for current_char in file_path[::-1]:
            if current_char == ".":
                extension_found = True
                break
            extension_index -= 1
        if not extension_found:
            raise ValueError("The file at '{}' does not have an extension".format(file_path))
        file_extension = file_path[extension_index - 1::]
        if not file_extension in self._SUPPORTED_FILES:
            raise ValueError("{} files are not supported".format(file_extension))
        return file_extension
        
    def get_yes_no_response(self, prompt):          
        valid_response = False
        while not valid_response:
            try:               
                response = input(prompt)
                if (not(self.is_yes_no_response(response))):
                    raise ValueError("Please enter yes or no")
                valid_response = True
            except ValueError as e:
                print("{}".format(e))
        return response;
    
    def is_yes_no_response(self, response):
        return response.lower() == "yes" or response.lower() == "no"
    
    def load(self):
        file_loaded = False
        response = self.get_yes_no_response("Would you like to load an excel file? (Yes/No)\n")
        if response.lower() == "yes":
            while not file_loaded:
                try:
                    file_path = input("Enter the path to the file you wish to load:\n")
                    data = self.load_file(file_path)
                    self._manager = AssetManager(data)
                    file_loaded = True
                except (ValueError, FileNotFoundError) as e:
                    print("{}".format(e))
                    response = self.get_yes_no_response("Would you like to try loading a different file? (Yes/No)\n")
                    if response == "no":
                        file_loaded = True
        self.run()
    
    def load_file(self, file_path):
        """
        
        raises:
            ValueError: If the file being loaded is not supported
            FileNotFoundError: If the file at the file_path does not exist
        """
        file_extension = self.get_file_extension(file_path)
        try:
            if file_extension == ".xlsx" or file_extension == ".xls":
                data = pd.read_excel(file_path)
            elif file_extension == ".csv":
                data = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("The file {} does not exist".format(file_path))
        return data
            
    def main(self):       
        """
        The main method which handles the program control flow
        """
        self.load()
        #self.data = pd.read_excel("Spreadsheets/demoAssets.xlsx")
        self.run()
    
    def run(self):
        pass
    
IO().main()