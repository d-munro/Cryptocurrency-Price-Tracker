# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:32:04 2022

@author: Dylan Munro
"""

import src.assets.manager as manage
import tests.data_test

from typing import Final

import pandas as pd

"""
Handles all IO requests from the user

class variables:
    file - The file which stores asset data if not using coingecko API
"""
class IO:
    
    #Final means static class checkers wont reassign. Must import Final from typing
    _SUPPORTED_FILES:Final = {".csv", ".xlsx"}
    
    def __init__(self):
        self._driver = None
        
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
                if (not(response.lower() == "yes" or response.lower() == "no")):
                    raise ValueError("Please enter yes or no")
                valid_response = True
            except ValueError as e:
                print("{}".format(e))
        return response;
    
    def load(self):
        """
        Loads all preliminary data required for program operation
        """
        file_loaded = False
        response = self.get_yes_no_response("Would you like to load an excel file? (Yes/No)\n")
        if response.lower() == "yes":
            while not file_loaded:
                try:
                    file_path = input("Enter the path to the file you wish to load:\n")
                    df = self.load_file(file_path)
                    self._driver = manage.Driver(df)
                    file_loaded = True
                except (ValueError, FileNotFoundError) as e:
                    print("{}".format(e))
                    response = self.get_yes_no_response("Would you like to try loading a different file? (Yes/No)\n")
                    if response == "no":
                        file_loaded = True
    
    def load_file(self, file_path):
        """
        Attempts to load the file at the given filepath
        
        Attributes:
            file_path - The path to the file
        
        raises:
            ValueError: If the file being loaded is not supported
            FileNotFoundError: If the file at the file_path does not exist
        """
        file_extension = self.get_file_extension(file_path)
        try:
            if file_extension == ".xlsx" or file_extension == ".xls":
                df = pd.read_excel(file_path)
            elif file_extension == ".csv":
                df = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("The file {} does not exist".format(file_path))
        return df
            
    def main(self):       
        """
        The main method which handles the program control flow
        """
        #self.load()
        self._driver = manage.Driver(self.load_file("resources/spreadsheets/functional.xlsx"))
        self.run()
        
    def run(self):
        user_response = 0
        prompt = self.get_prompt()
        assetless_requests = manage.Request.get_REQUESTS_NO_ASSETS()
        while not user_response == manage.Request.QUIT:
            try:
                #Name of the asset that the request is acting on
                asset_name = None
                
                user_response = int(input(prompt))
                if ((user_response < manage.Request.MIN_REQUEST_VALUE) 
                    or (user_response > manage.Request.MAX_REQUEST_VALUE)):
                    raise ValueError
                    
                #Obtain name of asset request is acting on if necessary
                if not user_response in assetless_requests:
                    asset_name = input("Enter the name of the asset:\n")
                    
                request = manage.Request(user_response, asset_name)
                print(self._driver.execute_request(request))
            except ValueError:
                print("Please enter a valid number")
    
    def get_prompt(self):
        """
        Returns all valid requests and their descriptions
        """
        requests = manage.Request.get_VALID_REQUESTS()
        key_list = list(requests.keys())
        temp = [""]
        for i in key_list:
            temp.append("Press ")
            temp.append(str(i))
            temp.append(" to ")
            temp.append(requests[i])
            temp.append("\n")
        return "".join(temp)

if __name__ == "__main__":
    IO().main()
    #tests.data_test.graph_tests()