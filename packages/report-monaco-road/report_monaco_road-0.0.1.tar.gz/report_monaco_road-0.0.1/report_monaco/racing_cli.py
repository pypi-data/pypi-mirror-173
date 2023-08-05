import os
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Racer:
    lap_time: str
    car: str
    driver: str


def validate_path(folder_path: str) -> str:
    data_folder = os.path.join(os.path.abspath('.'), folder_path)
    if not os.path.isdir(data_folder):
        raise FileNotFoundError('Folder not found')
    return str(data_folder)


def read_files(data_folder: str) -> List[List[str]]:
    data_from_files = []
    files = ["start.log", "end.log", "abbreviations.txt"]
    for file in files:
        file = os.path.join(data_folder, file)
        with open(file) as file_:
            data_from_files.append([line for line in file_ if line.strip() != ""])
    return data_from_files


def build_report(file_contents: list) -> List[Racer]:
    time_reg = '%H:%M:%S.%f'
    racer_data = []
    start_list, end_list, abbreviations_file = file_contents
    for start_item in start_list:
        end = str([end_time for end_time in end_list if (start_item[0:7] in end_time)])
        abbrev = [name.strip() for name in abbreviations_file if (start_item[0:3] in name)]
        lap_time = datetime.strptime(end[16:28], time_reg) - datetime.strptime(start_item[14:26], time_reg)
        if '-' not in str(lap_time):
            racer_data.append(Racer(str(lap_time), abbrev[0].split('_', 2)[2], abbrev[0].split('_', 2)[1]))
    return racer_data


def sort_data(racer_data: List[Racer], direction: bool) -> List[Racer]:
    return sorted(racer_data, key=lambda time: time.lap_time, reverse=direction)


def driver(racer_data: List[Racer], driver_name: str) -> List[Racer]:
    return [driver_info for driver_info in racer_data if driver_info.driver == driver_name]


def print_reports(sorted_data: List[Racer]) -> None:
    sorted_data = enumerate(sorted_data, start=1)
    for number, data_driver in sorted_data:
        if number == 16:                                # top 15 racers and the rest after underline
            print('_' * 40)
        print(f"{number}. {data_driver.driver}  | {data_driver.car}  | {data_driver.lap_time}")
