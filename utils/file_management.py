import os
import glob
import re
import shutil
import zipfile
from dotenv import load_dotenv


def find_file(pattern, folder):
    """
    Searches for a file matching a given regex pattern in the specified folder.

    Arguments:
    - pattern (str): The regex pattern to match file names.
    - folder (str): The folder to search in.

    Returns:
    - str or None: The name of the file if exactly one match is found, or None otherwise.
    """
    regex = re.compile(pattern, re.IGNORECASE)
    filesFound = []

    for root, _, files in os.walk(folder):
        for filename in files:
            if regex.match(filename):
                filesFound.append(filename)

    if len(filesFound) > 1:
        print(f"More than one file found matching pattern: {pattern}")
        return None
    elif len(filesFound) == 1:
        return filesFound[0]

    print(f"No file found matching pattern: {pattern}")
    return None


def get_excel_file(folder):
    """
    Returns the first .xlsx file found in the specified folder.

    Arguments:
    - folder (str): The folder to search in.

    Returns:
    - str or None: The path to the first Excel file found, or None if no Excel file is present.
    """
    files = glob.glob(os.path.join(folder, "*.xlsx"))
    return files[0] if files else None


def get_json_file(folder):
    """
    Returns the first .json file found in the specified folder.

    Arguments:
    - folder (str): The folder to search in.

    Returns:
    - str or None: The path to the first JSON file found, or None if no JSON file is present.
    """
    files = glob.glob(os.path.join(folder, "*.json"))
    return files[0] if files else None


def safe_folder_name(name):
    """
    Transforms a string into a safe folder name by replacing slashes and spaces.

    Arguments:
    - name (str): The original name.

    Returns:
    - str: The sanitized name, safe for use as a folder name.
    """
    return str(name).replace("/", "_").replace("\\", "_").replace(" ", "_")


def clear_folder(folder_path):
    """
    Deletes all contents (files and folders) inside the given folder path.

    Arguments:
    - folder_path (str): The folder to clear.
    """
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)


def load_env(caller_path):
    """
    Loads environment variables from a .env file located in the same directory as the given caller path.

    Arguments:
    - caller_path (str): The path of the file calling this function (usually __file__).
    """
    caller_dir = os.path.dirname(os.path.abspath(caller_path))
    env_path = os.path.join(caller_dir, ".env")
    load_dotenv(env_path)


def find_root_folder():
    """
    Prints the absolute path to the current script file.
    Mainly used for debugging or understanding where the script is running from.
    """
    print(os.path.abspath(__file__))


def group_files_in_single_folder(IN, OUT):
    """
    Parses files in a directory and its subdirectories,
    and copies them to a specified root directory.

    Arguments:
    - IN (str): The source directory to parse files from.
    - OUT (str): The root directory where files will be copied.
    """
    for root, _, files in os.walk(IN):
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(OUT, file)
            shutil.copy2(source_file_path, target_file_path)
            print(f"Copied {source_file_path} to {target_file_path}")


def zip_folder(folder_path, zip_path):
    """
    Zips the contents of a folder into a zip file.
    Arguments:
    - folder_path (str): The path to the folder to zip.
    - zip_path (str): The path where the zip file will be saved.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                if full_path == zip_path:
                    continue
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname)


def unzip_file(zip_path, extract_to):
    """
    Unzips a zip file to a specified directory.
    Arguments:
    - zip_path (str): The path to the zip file.
    - extract_to (str): The directory where the contents will be extracted.
    """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
