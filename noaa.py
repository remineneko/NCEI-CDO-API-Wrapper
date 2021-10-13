__author__ = "Hoang Tran"
__version__ = '1.1'

import requests
import datetime
from dateutil.relativedelta import relativedelta
import tabulate

BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/{}"


class Data(dict):
    def __init__(self, given_data:dict):
        super(dict, self).__init__()
        self._data = given_data

    def results_data(self):
        if 'results' in self._data:
            return self._data['results']
        else:
            return self._data

    def metadata(self):
        if 'metadata' in self._data:
            return self._data['metadata']
        else:
            raise KeyError("The given data does not have metadata as key")

    def __str__(self):
        if 'results' in self._data:
            actual_data = self._data['results']
            header = actual_data[0].keys()
            rows = [x.values() for x in actual_data]
        else:
            header = self._data.keys()
            rows = list(self._data.values())

        return tabulate.tabulate(rows, header)

    def __repr__(self):
        return self._data

    def __getitem__(self, item):
        return self._data[item]


class NOAA:
    def __init__(self, token):
        self._token = token

    @staticmethod
    def _date_validation(date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Date format should be YYYY-MM-DD")

    @staticmethod
    def _add_param(full_list, param_name, param_values):
        if type(param_values) == list:
            for elem in param_values:
                full_list.append('{}={}'.format(param_name, elem))
        elif type(param_values) == str or type(param_values) == int:
            full_list.append('{}={}'.format(param_name, str(param_values)))

    @staticmethod
    def _get_data(url, token):
        ans = requests.get(url, headers={
            'token': token
        })
        return Data(ans.json())

    def _list_checks(self, all_entries, kwargs, key_to_check):
        if key_to_check in kwargs:
            if type(kwargs[key_to_check]) != list:
                raise TypeError("{} should be declared as a list".format(key_to_check))
            elif len(kwargs[key_to_check]) != 0:
                self._add_param(all_entries, key_to_check.replace("_", ""), kwargs[key_to_check])

    def _make_url(self, url, kwargs, list_params, required_day=False):
        available_params = []
        if 'search_id' in kwargs and kwargs['search_id'] is not None:
            url += '/{}'.format(kwargs['search_id'])

        for id_type in list_params:
            self._list_checks(available_params, kwargs, id_type)

        supported_fields = ['id', 'name', 'mindate', 'maxdate', 'datacoverage']
        supported_sort_order = ['asc', 'desc']
        max_limit = 1000
        if not required_day:
            if 'start_date' in kwargs and kwargs['start_date'] is not None:
                self._date_validation(kwargs['start_date'])
                self._add_param(available_params, 'startdate', kwargs['start_date'])

            if 'end_date' in kwargs and kwargs['end_date'] is not None:
                self._date_validation(kwargs['end_date'])
                self._add_param(available_params, 'enddate', kwargs['end_date'])

        if 'sort_field' in kwargs and kwargs['sort_field'] is not None:
            if kwargs['sort_field'] not in supported_fields:
                raise ValueError("The value for sort_field is not supported.")
            else:
                self._add_param(available_params, 'sortfield', kwargs['sort_field'])

        if 'sort_order' in kwargs and kwargs['sort_order'] is not None:
            if kwargs['sort_order'] not in supported_sort_order:
                raise ValueError("The value for sort_order is not supported.")
            else:
                self._add_param(available_params, 'sortorder', kwargs['sort_order'])

        if 'limit' in kwargs and kwargs['limit'] is not None:
            if kwargs['limit'] > max_limit:
                raise ValueError("The limit value should not be higher than 1000")
            else:
                self._add_param(available_params, 'limit', kwargs['limit'])

        if 'offset' in kwargs and kwargs['offset'] is not None:
            self._add_param(available_params, 'offset', kwargs['offset'])

        url += '?' + '&'.join(available_params)
        return url

    def datasets(self, **kwargs):
        '''
        Obtains the information of the datasets from the NOAA.
        Users can optionally use different params to look into different data.
        Available params for kwargs:
            - search_id: The information of the ID that users want to look.
            - datatype_id: Optional. Accepts a list of data type ids.
            - location_id: Optional. Accepts a list of location ids.
            - station_id: Optional. Accepts a list of of station ids.
            - start_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - end_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - sort_field: Optional. The field to sort results by.
            Supported fields:
                + id
                + name
                + mindate
                + maxdate
                + datacoverage
            - sort_order: Optional. Which order to sort by, 'asc' or 'desc'. Defaults to 'asc'.
            - limit: Optional. Defaults to 25, limits the number of results in the response. Maximum is 1000.
            - offset: Optional. Defaults to 0, used to offset the resultlist.
        :return: The data from the given query, in json format.
        '''
        url = BASE_URL.format('datasets')
        list_entries = ['datatype_id', 'location_id', 'station_id']
        url = self._make_url(url, kwargs, list_entries)
        return self._get_data(url, self._token)

    def data_categories(self, **kwargs):
        '''
        Data Categories represent groupings of data types
        :param kwargs: Available params
            - search_id: The information of the ID that users want to look.
            - dataset_id: Optional. Accepts a list of dataset IDs.
            - location_id: Optional. Accepts a list of location ids.
            - station_id: Optional. Accepts a list of of station ids.
            - start_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - end_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - sort_field: Optional. The field to sort results by.
            Supported fields:
                + id
                + name
                + mindate
                + maxdate
                + datacoverage
            - sort_order: Optional. Which order to sort by, 'asc' or 'desc'. Defaults to 'asc'.
            - limit: Optional. Defaults to 25, limits the number of results in the response. Maximum is 1000.
            - offset: Optional. Defaults to 0, used to offset the resultlist.
        :return: The data from the given query, in json format.
        '''
        url = BASE_URL.format('datacategories')
        list_params = ['dataset_id', 'location_id', 'station_id']

        url = self._make_url(url, kwargs, list_params)

        return self._get_data(url, self._token)

    def datatypes(self, **kwargs):
        '''
        Available params:
            - search_id: The information of the ID that users want to look.
            - dataset_id: Optional. Accepts a list of dataset ids.
            - location_id: Optional. Accepts a list of location ids.
            - station_id: Optional. Accepts a list of of station ids
            - data_category_id: Optional. Accepts a list of data categories id.
            - start_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - end_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - sort_field: Optional. The field to sort results by.
            Supported fields:
                + id
                + name
                + mindate
                + maxdate
                + datacoverage
            - sort_order: Optional. Which order to sort by, 'asc' or 'desc'. Defaults to 'asc'.
            - limit: Optional. Defaults to 25, limits the number of results in the response. Maximum is 1000.
            - offset: Optional. Defaults to 0, used to offset the resultlist.
        :return: The data from the given query, in json format.
        '''
        url = BASE_URL.format('datatypes')
        list_params = ['dataset_id', 'location_id', 'station_id', 'data_category_id']

        url = self._make_url(url, kwargs, list_params)

        return self._get_data(url, self._token)

    def location_categories(self, **kwargs):
        '''
        Available params:
            - search_id: The information of the ID that users want to look.
            - dataset_id: Optional. Accepts a list of dataset ids.
            - start_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - end_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - sort_field: Optional. The field to sort results by.
            Supported fields:
                + id
                + name
                + mindate
                + maxdate
                + datacoverage
            - sort_order: Optional. Which order to sort by, 'asc' or 'desc'. Defaults to 'asc'.
            - limit: Optional. Defaults to 25, limits the number of results in the response. Maximum is 1000.
            - offset: Optional. Defaults to 0, used to offset the resultlist.
        :return: The data from the given query, in json format.
        '''
        url = BASE_URL.format('locationcategories')
        list_params = ['dataset_id']
        url = self._make_url(url, kwargs, list_params)
        return self._get_data(url, self._token)

    def locations(self, **kwargs):
        '''
        Available params for kwargs:
            - search_id: The information of the ID that users want to look.
            - dataset_id: Optional. Accepts a list of dataset ids.
            - datatype_id: Optional. Accepts a list of datatype ids.
            - data_category_id: Optional. Accepts a list of data categories id.
            - location_category_id: Optional. Accepts a list of of location categories ID.
            - start_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - end_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - sort_field: Optional. The field to sort results by.
            Supported fields:
                + id
                + name
                + mindate
                + maxdate
                + datacoverage
            - sort_order: Optional. Which order to sort by, 'asc' or 'desc'. Defaults to 'asc'.
            - limit: Optional. Defaults to 25, limits the number of results in the response. Maximum is 1000.
            - offset: Optional. Defaults to 0, used to offset the resultlist.
        :return: The data from the given query, in json format.
        '''
        url = BASE_URL.format('locations')
        list_params = ['dataset_id', 'location_category_id', 'data_category_id']
        url = self._make_url(url, kwargs, list_params)
        return self._get_data(url, self._token)

    def stations(self, **kwargs):
        '''
        Available params:
            - search_id: The information of the ID that users want to look.
            - dataset_id: The ID of the dataset that users want to look at.
            - datatype_id: Optional. Accepts a list of data type ids.
            - location_id: Optional. Accepts a list of location ids.
            - data_category_id: Optional. Accepts a list of data categories id.
            - extent: Optional. The desired geographical extent for search.
            Optimally, please input a list of four elements as follows:
                [east, north, south, west]
            - start_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - end_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - sort_field: Optional. The field to sort results by.
            Supported fields:
                + id
                + name
                + mindate
                + maxdate
                + datacoverage
            - sort_order: Optional. Which order to sort by, 'asc' or 'desc'. Defaults to 'asc'.
            - limit: Optional. Defaults to 25, limits the number of results in the response. Maximum is 1000.
            - offset: Optional. Defaults to 0, used to offset the resultlist.
        :return: The data from the given query, in json format.
        '''
        url = BASE_URL.format('stations')
        list_params = ['dataset_id', 'location_id', 'data_category_id', 'datatype_id']
        url = self._make_url(url, kwargs, list_params)
        if 'extent' in kwargs and type(kwargs['extent']) == list and len(kwargs['extent']) != 0:
            url += 'extent={}'.format(','.join([str(i) for i in kwargs['extent']]))
        return self._get_data(url, self._token)

    def data(self, dataset_id, start_date, end_date, **kwargs):
        '''
        Fetches the data from Climate Data Online dataset.
        :param dataset_id: The ID of the dataset that contains the desired data
        :param start_date: The starting date of the dataset
        :param end_date: The ending date of the dataset.
            Note that the difference in time must not exceed 10 years.
        :param kwargs: Available params:
            - datatype_id: Optional. Accepts a list of data type ids.
            - location_id: Optional. Accepts a list of location ids.
            - station_id: Optional. Accepts a list of of station ids.
            - start_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - end_date: Optional. Accepts valid ISO formatted date (yyyy-mm-dd).
            - units: Optional. Accepts either 'metric' or 'standard'.
            - sort_field: Optional. The field to sort results by.
            Supported fields:
                + id
                + name
                + mindate
                + maxdate
                + datacoverage
            - sort_order: Optional. Which order to sort by, 'asc' or 'desc'. Defaults to 'asc'.
            - limit: Optional. Defaults to 25, limits the number of results in the response. Maximum is 1000.
            - offset: Optional. Defaults to 0, used to offset the resultlist.
            - include_metadata: Optional. Defaults to 'true', used to improve response time by preventing the calculation
                of result metadata.
        :return: The data from the given query, in json format
        '''
        self._date_validation(start_date)
        self._date_validation(end_date)

        dt_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        dt_end = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        time_diff = relativedelta(dt_end, dt_start)

        if time_diff.years > 10 or (time_diff.years == 10 and (time_diff.months > 0 or time_diff.days > 0)):
            raise ValueError("The difference should be 10 years")

        url = BASE_URL.format('data?datasetid={}&startdate={}&enddate={}'.format(dataset_id, start_date, end_date))
        list_params = ['datatype_id', 'location_id', 'station_id']
        url = self._make_url(url, kwargs, list_params, required_day=True)

        accepted_units = ['standard', 'metric']
        if 'units' in kwargs and kwargs['units'] in accepted_units:
            url += '&units={}'.format(kwargs['units'])

        accepted_metadata_choices = ['true', 'false']
        if 'include_metadata' in kwargs and kwargs['include_metadata'] in accepted_metadata_choices:
            url += '&includemetadata={}'.format(kwargs['include_metadata'])
        return self._get_data(url, self._token)
