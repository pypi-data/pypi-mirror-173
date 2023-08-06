import json
import requests
import typing
from erddapy import ERDDAP
from erddapy.erddapy import parse_dates
from datetime import datetime
from app_common.utilities.time_format_functions import str_to_timeobj

one_day_in_sec = 86400


def request_json_data(url: str) -> dict:
    r = requests.get(url)
    content = {}
    if r.status_code == 200:
        content = json.loads(r.content.decode('utf-8'))
    return content


class ErddapProxy(ERDDAP):
    SAMPLE_SECS = one_day_in_sec

    def __init__(self, host, protocol="tabledap"):
        super().__init__(host, protocol=protocol)

    @staticmethod
    def get_dataset_id_filter(rows_line):
        dataset_ids = []
        for row in rows_line:
            dataset_ids.append(row[0])
        return dataset_ids

    def get_dataset_ids(self) -> list:
        all_datasets_url = self.get_download_url(dataset_id="allDatasets", response="json", protocol="tabledap",
                                                 variables=["datasetID",
                                                            "title"])
        json_output = request_json_data(all_datasets_url)
        rows = json_output["table"]["rows"]
        glider_id_list = self.get_dataset_id_filter(rows)
        return glider_id_list

    def get_modified_date(self, dataset_id):
        variables = self._get_variables(dataset_id)
        global_variable = variables["NC_GLOBAL"]
        return global_variable["date_modified"]

    def get_time_coverage_start_end(self, dataset_id):
        variables = self._get_variables(dataset_id)
        global_variable = variables["NC_GLOBAL"]
        return global_variable["time_coverage_start"], global_variable["time_coverage_end"]

    def get_one_day_timestamp_range_generator(self, time_coverage_start_timestamp, time_coverage_end_timestamp):
        first_timestamp = time_coverage_start_timestamp
        while first_timestamp < time_coverage_end_timestamp:
            second_timestamp = first_timestamp + self.SAMPLE_SECS
            yield first_timestamp, second_timestamp
            first_timestamp = second_timestamp

    def get_dataset_one_day_sample_download_url_generator(self, dataset_id: str):
        """
        This function can generate erddap dataset url for given dataset id day by day.
        :param dataset_id:
        :return:
        """
        time_coverage_start_str, time_coverage_end_str = self.get_time_coverage_start_end(dataset_id)
        time_coverage_start_timestamp = parse_dates(time_coverage_start_str)
        time_coverage_end_timestamp = parse_dates(time_coverage_end_str)
        for first_timestamp, second_timestamp in self.get_one_day_timestamp_range_generator(
                time_coverage_start_timestamp,
                time_coverage_end_timestamp):
            download_url = self.get_download_url(dataset_id=dataset_id, protocol="tabledap", response='nc',
                                                 constraints={
                                                     "time>=": datetime.fromtimestamp(first_timestamp),
                                                     "time<=": datetime.fromtimestamp(
                                                         second_timestamp)})
            yield download_url
