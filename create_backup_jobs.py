"""Creates the backup 'definition' files for each 'job' written by NSGLABS on 5/7/25"""

from tkinter import filedialog
import tkinter as tk
import pyinputplus as pyin
import csv, os

jobs_path = os.path.join(os.getcwd(), 'Jobs')
if not os.path.exists(jobs_path):
    os.makedirs(jobs_path)


def get_dir():
    """Returns path for src and dst locations."""
    file_path = filedialog.askdirectory(title = "Select your location.")
    return file_path


def source_location():
    """Selects the source dir to backup"""
    print('Select your source file path.\n')

    root = tk.Tk()
    root.withdraw()

    while True:
        source_path = get_dir()
        print(f'Is the src path at {source_path} correct?')
        path_correct = pyin.inputMenu(['Y', 'N', 'Q']).lower()
        if path_correct == 'n':
            continue

        elif path_correct == 'y':
            print(f'Continuing with src path at {source_path}')
            return source_path

        elif path_correct == 'q':
            print('Exiting')
            exit()

def destination_location():
    """Selects the destination dir to backup to."""
    print('Select your dst file path.\n')

    root = tk.Tk()
    root.withdraw()

    while True:
        destination_path = get_dir()
        print(f'Is the dst path at {destination_path} correct?')
        path_correct = pyin.inputMenu(['Y', 'N', 'Q']).lower()
        if path_correct == 'n':
            continue

        elif path_correct == 'y':
            print(f'Continuing with dst path at {destination_path}')
            return destination_path

        elif path_correct == 'q':
            print('Exiting')
            exit()

def csv_job_write():
    """Write the 'job definition' to the csv file"""

    csv_file_path = os.path.join(os.getcwd(), r'Jobs\jobs.csv')

    # Check if file exists and is empty
    file_exists = os.path.isfile(csv_file_path)
    file_empty = not os.path.getsize(csv_file_path) if file_exists else True

    with open(csv_file_path, mode = 'a', newline='') as file:
        writer = csv.writer(file)

        # Write header if file is new or empty
        if file_empty:
            writer.writerow(["Source", "Dest"])

        writer.writerow([src_path, dst_path])


src_path = source_location()
dst_path = destination_location()

csv_job_write()
print('Jobs successfully created.')
