"""Runs the backups jobs at Jobs\jobs.csv written by NSGLABS on 5/7/25"""

import os, csv, subprocess, zipfile, shutil, datetime


src = []
dst = []

temp_dir = os.path.join(os.getcwd(), 'temp')


if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


def get_jobs():
    """Reads the jobs.csv file"""

    global src
    global dst

    jobs_path = os.path.join(os.getcwd(), r'Jobs\dbjob.csv')

    # Check if file exists
    file_exists = os.path.isfile(jobs_path)
    if not file_exists:
        print('Jobs file does not exist. Please run CreateJobs.bat before continuing')
        quit()
    else:
        print('Jobs file found.')


    # Read csv file
    with open(jobs_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src.append(row['Source'])
            dst.append(row['Dest'])


def clear_temp_files():
    """Removes files from the temp folder"""

    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        try:
            if os.path.isdir(item_path):
                if item == '.git':
                    continue
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        except PermissionError as e:
            print(f"Skipping {item_path}: {e}")


def zip_files(zip_path):
    """Used to zip files in the temp dir."""

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname=relative_path)


def copy_to_temp():
    """Copies files to temp folder to zip"""

    for jobs in range(len(src)):
        print(f"Copying from: {src[jobs]} to {temp_dir}")
        clear_temp_files()

        
        try:
            result = subprocess.run(["robocopy", src[jobs], temp_dir, "/E", "/R:3", "/W:10"], check=True, capture_output=True, text=True)
            print("Robocopy completed successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Robocopy failed with error code {e.returncode}:")
            print(e.stderr)
        except FileNotFoundError:
            print("Robocopy command not found. Make sure it's in your system's PATH.")

        # zip the files
        if not os.path.exists(dst[jobs]):
            os.makedirs(dst[jobs])
        zip_name = f"DB_backup_{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.zip"
        zip_path = os.path.join(dst[jobs], zip_name)

        zip_files(zip_path)


get_jobs()
copy_to_temp()
