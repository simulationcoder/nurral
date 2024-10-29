#Importing all modules required for this class
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

class Currency:
    """
    The Currency class provides a method for retrieving foreign exchange (FX) rates from various data sources, 
    such as Google Sheets. The method supports filtering data by date, extracting specific numbers of rows from the dataset, 
    and limiting the results to particular currency pairs.
    """

    @staticmethod
    def getFxRate(**kwargs):
        """
        This is the main method that retrieves the FX rates. It accepts several keyword arguments that allow the 
        user to specify the data source, the provider of the exchange rates, and other optional filters like date ranges 
        and the number of rows to extract.

        Parameters
            database: (str, optional)
            The source of the FX rate data. Currently supported value: 'googleSheets'.

        provider: (str, optional)
            The provider of the FX rate data. Currently supported value: 'BoC' (Bank of Canada).

        typeof: (str, optional)
            The type of FX rate to retrieve. Supported value: 'spot'.

        currencyPairs: (list or str, optional)
            A list of currency pairs to filter the data. Default is 'All' (i.e., no filtering by currency pair).

        startDate: (str, optional)
            The start date for filtering data, typically in YYYY-MM-DD format.

        endDate: (str, optional)
            The end date for filtering data, typically in YYYY-MM-DD format.

        allDates: (str, optional)
            If set to 'Yes', the method will return all available data without filtering by date. Default is None.

        headRows: (int, optional)
            The number of top rows to extract from the dataset.

        tailRows: (int, optional)
            The number of bottom rows to extract from the dataset.

        Returns
            sub_extract: (pandas.DataFrame)
            A DataFrame containing the extracted FX rate data filtered by the input parameters.

        value: (int)
            An integer code indicating the success or failure of the query:
        
        exitPhrase: (str)
            A descriptive message explaining the value result.
            0: Something went wrong in the query.
            1: Query successful.
            2: Currency pairs not found.
            3: More conditions are required to filter the data.
        
        Workflow
            Error Handling: A set of error codes and messages (returnValues) are predefined to track the success or failure of the query.

        URL Extraction:
            If the database is set to 'googleSheets', provider is 'BoC', and typeof is 'spot', the method reads a CSV file (finDataReaderLinks.csv) to obtain the URL of the Google Sheets dataset.

        Data Extraction:
            The data from the Google Sheets URL is extracted into a DataFrame (extract).

        Filtering Data:
            The method supports the following data filters:

        Extract all data if allDates is set to 'Yes'.
        Extract a specific number of rows using headRows or tailRows.
        Extract data within a date range using startDate and endDate.

        Condition - Start Date Provided, End Date not provided:
        If startDate is provided and endDate is None, the code filters the data starting from startDate to the end of the dataset (extract.loc[startDate:]).
        The loc[startDate:] syntax selects all rows starting from startDate to the last available date in the dataset.
        
        Condition - Start Date None, End Date Provided:
        If startDate is None but endDate is provided, the code sets the startDate to the first available date in the dataset (extract.index.min()),
        assuming the dataset index contains dates.
        The code then filters the data from this earliest date (startDate) to the provided endDate using loc[startDate:endDate]

        validate_date Function: A helper function that uses datetime.strptime to check whether a 
        date string is in the correct format ('%Y-%m-%d'). It returns True if valid and False if not.
        
        Currency Pair Filtering:
            If specific currency pairs are provided (currencyPairs), the method filters the DataFrame accordingly.

        Return:
            The filtered DataFrame, along with the value code and an explanatory exitPhrase, is returned.   
        
        Usage examples:
        (1) currency_data, status, message = Currency.getFxRate(
            database='googleSheets', 
            provider='BoC', 
            typeof='spot', 
            currencyPairs=['USD/CAD'], 
            startDate='2023-01-01', 
            endDate='2023-12-31')     

        (2) currency_data, status, message = Currency.getFxRate(
            database='googlesheets',
            provider='BoC',
            typeof='spot',
            tailRows=10,
            currencyPairs=['AUDCAD','INRCAD'])

        (3) currency_data, status, message = Currency.getFxRate(
            database='googlesheets',
            provider='BoC',
            typeof='spot',
            tailRows=10)
        
        (4) currency_data, status, message = Currency.getFxRate(
            database='googlesheets',
            provider='BoC',
            typeof='spot',
            allDates="Yes",
            currencyPairs=['AUDCAD','INRCAD'])
        
        (5) currency_data, status, message = Currency.getFxRate(
            database='googleSheets',
            provider='BoC',
            typeof='spot',
            startDate="2024-01-01",
            endDate='2024-09-19',
            currencyPairs=['AUDCAD','INRCAD'])
 
        """
        database=   kwargs.get('database',None)             #database - googlesheets, onedrive, etc
        provider=   kwargs.get('provider',None)             #provider - BoC, etc
        typeof=     kwargs.get('typeof',None)               #typeof - spot or forward 
        currencyPairs=  kwargs.get('currencyPairs','All')   #List of currency pairs
        startDate=  kwargs.get('startDate',None)            #start date
        endDate=    kwargs.get('endDate',None)              #end date
        allDates=   kwargs.get('allDates',None)             #extract all dates
        headRows=   kwargs.get('headRows',None)             #expects a number, the number signifies, how many rows from the top does the user wants
        tailRows=   kwargs.get('tailRows',None)             #expects a number, the number signifies, how many rows from the bottom does the user wants

         # Log the received parameters
        logging.info(f"Received parameters: database={database}, provider={provider}, type={typeof}, "
                     f"currencyPairs={currencyPairs}, startDate={startDate}, endDate={endDate}, "
                     f"allDates={allDates}, headRows={headRows}, tailRows={tailRows}")

        #Error codes used below
        returnValues={0:'Something wrong in the query',
              1:'Query Successful',
              2:'Currency Pairs not found',
              3:'More conditions required',
              4:'Invalid date format'}
        
        #empty variables used below
        extract=pd.DataFrame()
        sub_extract=pd.DataFrame()
        value=0
        exitPhrase=''

        #Helper function to validate date format
        def validate_date(date_str):
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return True
            except ValueError:
                return False

        # Validate startDate and endDate if provided
        if startDate is not None and not validate_date(startDate):
            logging.error(f"Invalid date format for startDate: {startDate}. Expected format is yyyy-mm-dd.")
            value = 4
            exitPhrase = returnValues[value]
            return sub_extract, value, exitPhrase

        if endDate is not None and not validate_date(endDate):
            logging.error(f"Invalid date format for endDate: {endDate}. Expected format is yyyy-mm-dd.")
            value = 4
            exitPhrase = returnValues[value]
            return sub_extract, value, exitPhrase
        
        # Check if conditions for googleSheets and BoC spot rates are met
        if database=='googleSheets' and provider=='BoC' and typeof=='spot':
            try:
                #extracting the Workbook link
                base_dir = Path(__file__).resolve().parent
                linksFilePath = base_dir / 'csv' / 'finDataReaderLinks.csv'
                linksFile=pd.read_csv(linksFilePath)
                
                url=linksFile.loc[(linksFile['database']==database) 
                                & (linksFile['provider']==provider) 
                                & (linksFile['type']==typeof),'csvLink'].iloc[0]
                
                logging.info(f"Extracting data from URL: {url}")

                #read the data from the url
                extract = pd.read_csv(url,index_col=0)

                if allDates=='Yes':
                    #extract data for all the dates
                    logging.info("Extracting all data (no date filtering)")
                    sub_extract = extract               #assigning the extract to subextract to maintain a pattern
                    value=1                             #value = 1 Means that the query is successful
                    exitPhrase = returnValues[value]    #exit phrase explains the meaning of the value variable
                elif headRows is not None and isinstance(headRows,(int,float,complex)):
                    #extract top x number of rows from the dataset
                    logging.info(f"Extracting the first {headRows} rows from the data")
                    sub_extract = extract.head(headRows)
                    value=1
                    exitPhrase = returnValues[value]
                elif tailRows is not None and isinstance(tailRows,(int,float,complex)):
                    #extract last x number of rows
                    logging.info(f"Extracting the last {tailRows} rows from the data")
                    sub_extract=extract.tail(tailRows)
                    value=1
                    exitPhrase=returnValues[value]
                elif startDate is not None and endDate is None:
                    # Condition 1: Filter data from startDate to the end of the extract
                    logging.info(f"Filtering data from {startDate} to the end of the dataset")
                    sub_extract = extract.loc[startDate:]
                    value = 1
                    exitPhrase=returnValues[value]
                elif startDate is None and endDate is not None:
                    # Condition 2: Set startDate to the first available date in the dataset
                    logging.info(f"No startDate provided. Setting startDate to the first available date in the dataset")
                    startDate = extract.index.min()  # Assume the index contains dates
                    logging.info(f"Filtering data from {startDate} to {endDate}")
                    sub_extract = extract.loc[startDate:endDate]
                    value = 1
                    exitPhrase=returnValues[value]
                elif startDate is not None and endDate is not None:
                    #extract data between two dates
                    logging.info(f"Filtering data between {startDate} and {endDate}")
                    value=1
                    sub_extract=extract.loc[startDate:endDate]
                else:
                    #none of the above conditions were met, so exiting the loop with error code 3
                    logging.warning("Insufficient conditions provided for data extraction")
                    value=3
                    exitPhrase=returnValues[value]
            except Exception as e:
                logging.error(f"Error extracting data: {e}")
                value = 0
        else:
            #the database, provider and typeof variables dont meet the condition. This can be used to add future options
            logging.warning("Invalid combination of database, provider, or type")
            value=0
            exitPhrase=returnValues[value]
        
        if value != 0 and currencyPairs != 'All':
            try:
                if isinstance(currencyPairs, list):
                    # Use a list comprehension to remove '/' or other special characters from each pair
                    logging.info("Cleaning currency pairs to remove special characters")
                    currencyPairs = [pair.replace('/', '') for pair in currencyPairs]

                    # Attempt to filter the DataFrame by the given currency pairs
                    logging.info(f"Filtering data by currency pairs: {currencyPairs}")
                    sub_extract = sub_extract[currencyPairs]
                    value = 1
                    exitPhrase = returnValues[value]
            except KeyError as e:
                # Handle the case where the currency pairs do not exist in the dataset
                logging.error(f"Currency pairs not found: {currencyPairs}")
                sub_extract = pd.DataFrame()
                value = 2  # Currency Pairs not found
                exitPhrase = f"Currency Pairs not found: {e}"
            except Exception as e:
                # Catch any other unexpected errors
                logging.error(f"Unexpected error during currency pair filtering: {e}")
                sub_extract = pd.DataFrame()
                value = 0  # Generic error code
                exitPhrase = f"An unexpected error occurred: {e}"
        
        # Log the final status of the query
        exitPhrase = returnValues.get(value, 'Unknown error')
        logging.info(f"Query result: {exitPhrase} (value={value})")

        #returning the dataset with exit phrase and exit codes
        return sub_extract,value,exitPhrase