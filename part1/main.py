import concurrent.futures
import os
import shutil


def parse_input():
    source_folder = input("Add source folder: ")
    if not os.path.isdir(source_folder):
        raise NotADirectoryError(f"Source folder '{source_folder}' does not exist.")

    destination_folder = input("Add destination folder: ")
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
        print(f"Folder {destination_folder} was created")

    return source_folder, destination_folder


def get_extension(file_path):
    return os.path.splitext(file_path)[1].lstrip('.').lower()


def process_single_file(source_file_path, destination_folder):
    file_name = os.path.basename(source_file_path)
    file_extension = get_extension(source_file_path)

    extension_dir = os.path.join(destination_folder, file_extension)
    os.makedirs(extension_dir, exist_ok=True)

    destination_file_path = os.path.join(extension_dir, file_name)
    shutil.copy2(source_file_path, destination_file_path)


def process_directory(source_folder, destination_folder):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                executor.submit(process_single_file, source_file_path, destination_folder)


if __name__ == "__main__":
    try:
        source, destination = parse_input()
        process_directory(source, destination)
        print("File processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")