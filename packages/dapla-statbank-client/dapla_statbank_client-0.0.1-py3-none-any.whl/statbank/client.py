#!/usr/bin/env python3

from .auth import StatbankAuth
from .uttrekk import StatbankUttrekksBeskrivelse
from .transfer import StatbankTransfer
from .apidata import apidata_all, apidata

import datetime
from datetime import timedelta as td
import pandas as pd
import ipywidgets as widgets
import os

class StatbankClient(StatbankAuth):
    """
    This is the main interface towards the rest of the statbank-package.
    An initialized client, an object of this class, will contain data/parameters
    that often is shared, among all transfers within a statistical production.
    Call methods under this client to:
    - transfer the data
        .transfer()
    - only validate the data against a description
        .validate()
    - get transfer/data description (filbeskrivelse)
        .get_description()
    - set the publish date with a datepicker
        .date_picker() + .set_publish_date()
    - get published data from the external or internal API of statbanken
        apidata_all() / apidata()
    ...

    Attributes
    ----------
    loaduser : str
        Username for Statbanken, not the same as "tbf" or "common personal username" in other SSB-systems
    date : str
        Date for publishing the transfer. Shape should be "yyyy-mm-dd", like "2022-01-01". 
        Statbanken only allows publishing four months into the future?
    shortuser : str
        The abbrivation of username at ssb. Three letters, like "cfc".
        If not specified, we will try to get this from daplas environement variables.
    cc : str
        First person to be notified by email of transfer. Defaults to the same as "shortuser"
    bcc : str
        Second person to be notified by email of transfer. Defaults to the same as "cc"
    overwrite : bool
        False = no overwrite
        True = overwrite
    approve : str
        "0" = manual approval
        "1" = automatic approval at transfer-time (immediately)
        "2" = JIT (Just In Time), approval right before publishing time
    validation : bool
        Set to True, if you want the python-validation code to run user-side.
        Set to False, if its slow and unnecessary.
    log: list
        Each "action" (method used) on the client is appended to the log.
        Nice to use for appending to your own logging after you are done,
        or printing it in a try-except-block to see what the last actions were,
        before error being raised.

    Methods
    -------
    get_description(tableid):
        Get the "uttrekksbeskrivelse" for the tableid, which describes metadata
        about shape of data to be transferred, and metadata about the table
        itself in Statbankens system, like ID, name and content of codelists.
        Returns an object of the internal class "StatbankUttrekksBeskrivelse"
    validate(data, tableid):
        Gets an "uttrekksbeskrivelse" and validates the data against this.
        All validation happens locally, so dont be afraid of any data
        being sent to statbanken using this method.
        Logic is built in Python, and can probably be expanded upon.
    transfer(data, tableid):
        Transfers your data to Statbanken.
        First it gets an uttrekksbeskrivelse, validates against this,
        then makes the actual transfer. Validation can be set to False,
        to avoid this checking beforehand. 
        Make sure you've set the publish-date correctly before sending.

    date = date_picker():
        Shows a date-picker widget using ipywidget.
    set_publish_date(date):
        To actually set the date,
        the result of the picker must be sent into this function after editing.
        This method also excepts a datetime, datetime.date,
        or a string in the format YYYY-mm-dd.

    apidata_all(tableid):
        Finds "all the codes" of data for the table, using a first request.
        Then builds a query from this to get all the data using apidata().
        Use this if you want "all the data" from a table, and this isnt too big.
    apidata(tableid, query):
        Lets you specify a query, to limit the data in the response. 
        Get this query from the bottom of the statbank-webpage (API-spørring).


    get_description_batch(tableids):
        Send in a list of tableids: ['00000', '00000'].
        Returns a list of StatbankUttrekksBeskrivelse,
        which you may inspect / use as you wish.
    validate_batch({tableids:datas}):
        Send in a dict of tableids as keys, and data as lists/dataframes in the dict values.
        Will validate all in the list, until one returns an error.
    transfer_batch({tableids:datas}):
        Send in a dict of tableids as keys, and data as lists/dataframes in the dict values.
        Will try to transfer all of them, until it reaches an error.
        Publishing a table to statbanken many times before the publishing date is ok.
        But if you do it too fast, in succession, you might encounter an error like
        "ikke unik skranke" or similar.

    __init__():
        Sets attributes, validates them, builds header, initializes log.
    
    """
    
    
    def __init__(self,
            loaduser = "",
            date: datetime.datetime = datetime.datetime.now() + td(days=1),
            shortuser: str = "",
            cc: str = "",
            bcc: str = "",
            overwrite: bool = True,
            approve: str = '2',
            validation: bool = True,
            ):
        self.loaduser = loaduser
        self.date = date
        self.shortuser = shortuser
        self.cc = cc
        self.bcc = bcc
        self.overwrite = overwrite
        self.approve = approve
        self.validation = validation
        self._validate_params_init()
        self.__headers = self._build_headers()
        self.log = []

    # Representation
    def __str__(self):
        return f'''StatbankClient for user {self.loaduser}
        Publishing at {self.date}
        Shortuser {self.shortuser}
        Sending mail to {self.cc}
        And sending mail to {self.bcc}
        Overwrite set to {self.overwrite}
        Approve set to {self.approve}
        Validation set to {self.validation}
        
        Log:
        ''' + "\n\t".join(self.log)

    def __repr__(self):
        return f'StatbankClient(loaduser = "{self.loaduser}")'
    
    # Publishing date handeling
    def date_picker(self) -> None:        
        datepicker =  widgets.DatePicker(
            description='Publish-date',
            disabled=False,
            value=self.date
        )
        display(datepicker)
        self.log.append(f'Datepicker created at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        return datepicker

    def set_publish_date(self, date: datetime.datetime) -> None:
        if isinstance(date, widgets.widget_date.DatePicker):
            self.date = date.value
        elif isinstance(date, str):
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            self.date = date
        print("Publishing date set to:", self.date)
        self.log.append(f'Date set to {self.date} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        #return self.date

    # Descriptions
    def get_description(self, tableid: str = "00000") -> StatbankUttrekksBeskrivelse:
        self._validate_params_action(tableids=[tableid])
        self.log.append(f'Getting description for tableid {tableid} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        return StatbankUttrekksBeskrivelse(tabellid=tableid,
                                          loaduser=self.loaduser,
                                          headers=self.__headers)
    
    
    def get_description_batch(self, tableids: list) -> dict:
        self._validate_params_action(tableids=tableids)
        descriptions = {}
        for tableid in tableids:
            descriptions[tableid] = StatbankUttrekksBeskrivelse(tabellid=tableid,
                                        loaduser=self.loaduser,
                                        headers=self.__headers)
            self.log.append(f'Got description for tableid {tableid} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        return descriptions
    
    # Validation
    def validate(self, 
                 dfs: pd.DataFrame, 
                 tableid: str = "00000",
                 raise_errors: bool = False) -> dict:
        self._validate_params_action([tableid])
        validator = StatbankUttrekksBeskrivelse(tabellid=tableid,
                                        loaduser=self.loaduser,
                                        raise_errors=raise_errors,
                                        headers=self.__headers)
        validator.validate_dfs(dfs)
        self.log.append(f'Validated data for tableid {tableid} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')

    def validate_batch(self, data: dict, raise_errors: bool = False) -> dict:
        self._validate_params_action(list(data.keys()))
        validators = {}
        for tableid, dfs in data.items():
            validator = StatbankUttrekksBeskrivelse(tabellid=tableid,
                                        loaduser=self.loaduser,
                                        raise_errors=raise_errors,
                                        headers=self.__headers)
            validator.validate_dfs(dfs)
            self.log.append(f'Validated data for tableid {tableid} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')

    # Transfers
    def transfer(self,
                 dfs: pd.DataFrame, 
                 tableid: str = "00000") -> StatbankTransfer:
        self._validate_params_action([tableid])
        self.log.append(f'Transferring tableid {tableid} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        return StatbankTransfer(dfs,
                                tabellid=tableid,
                                loaduser=self.loaduser,
                                headers=self.__headers,
                                bruker_trebokstaver=self.shortuser,
                                publisering=self.date,
                                fagansvarlig1=self.cc,
                                fagansvarlig2=self.bcc,
                                auto_overskriv_data=str(int(self.overwrite)),
                                auto_godkjenn_data=self.approve,
                                validation=self.validation,
                               )

    def transfer_batch(self, data: dict) -> dict:
        self._validate_params_action(list(data.keys()))
        transfers = {}
        for tableid, dfs in data.items():
            transfers[tableid] = StatbankTransfer(dfs,
                                                  tabellid=tableid,
                                                  loaduser=self.loaduser,
                                                  headers=self.__headers,
                                                  bruker_trebokstaver=self.shortuser,
                                                  publisering=self.date,
                                                  fagansvarlig1=self.cc,
                                                  fagansvarlig2=self.bcc,
                                                  auto_overskriv_data=str(int(self.overwrite)),
                                                  auto_godkjenn_data=self.approve,
                                                  validation=self.validation,)
            self.log.append(f'Transferred tableid {tableid} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
        return transfers
    
    # Get apidata
    def apidata(id_or_url: str = "",
                payload: dict = {"query": [], "response": {"format": "json-stat2"}},
                include_id: bool = False) -> pd.DataFrame:
        """
        Parameter1 - id_or_url: The id of the STATBANK-table to get the total query for, or supply the total url, if the table is "internal".
        Parameter2: Payload, the query to include with the request.
        Parameter3: If you want to include "codes" in the dataframe, set this to True
        Returns: a pandas dataframe with the table
        """
        return apidata(id_or_url, payload, include_id)
    
    def apidata_all(id_or_url: str = "",
                include_id: bool = False) -> pd.DataFrame:
        """
        Parameter1 - id_or_url: The id of the STATBANK-table to get the total query for, or supply the total url, if the table is "internal".
        Returns: a pandas dataframe with the table
        """
        return apidata_all(id_or_url, include_id)
    
    
    # Class meta-validation
    def _validate_params_action(self, tableids: list) -> None:
        for tableid in tableids:
            if not isinstance(tableid, str):
                raise TypeError(f"{tableid} is not a string.")
            if not len(tableid) == 5:
                raise ValueError(f"{tableid} is not 5 characters long.")

    def _validate_params_init(self) -> None:
        if not self.loaduser or not isinstance(self.loaduser, str):
            raise TypeError('Please pass in "loaduser" as a string.')
        if not self.shortuser:
            self.shortuser = os.environ['JUPYTERHUB_USER'].split("@")[0]
        if not self.cc:
            self.cc = self.shortuser
        if not self.bcc:
            self.bcc = self.cc
        if not isinstance(self.overwrite, bool):
            raise ValueError("(Bool) Set overwrite to either False = no overwrite (dublicates give errors), or  True = automatic overwrite")
        if self.approve not in ['0', '1', '2']:
            raise ValueError("(String) Set approve to either '0' = manual, '1' = automatic (immediatly), or '2' = JIT-automatic (just-in-time)")