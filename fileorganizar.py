import os
import shutil
from datetime import datetime

def get_file_type(filename):
    """Returns the file extension as its 'type' (e.g., '.pdf', '.jpg')."""
    return os.path.splitext(filename)[1].lower() or "no_extension"

def get_creation_date(filepath):
    """
    Attempts to get the file's creation date.
    Falls back to modification date if creation date is not available or reliable.
    Returns a datetime object.
    """
    try:
        # On some systems (like Linux), st_birthtime (creation time) might not be available.
        # So we try it first, then fall back to st_mtime (modification time).
        timestamp = os.path.getctime(filepath)
    except AttributeError:
        timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp)

def organize_files(source_folder, destination_folder, organize_by_month=False):
    """
    Organizes files from a source folder into a destination folder.
    Structure: destination_folder/FileType/Year/Month/filename or destination_folder/FileType/Year/filename
    """
    if not os.path.isdir(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created destination folder: '{destination_folder}'")

    print(f"\nScanning files in '{source_folder}' for organization...")
    files_moved_count = 0
    errors_count = 0

    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)

        if os.path.isfile(source_path):
            file_type = get_file_type(item).lstrip('.') # Remove leading dot for folder name
            if not file_type: # Handle cases where get_file_type might return empty string
                file_type = "unknown_type"

            try:
                file_date = get_creation_date(source_path)
                year = file_date.strftime("%Y")
                month = file_date.strftime("%m - %B") # e.g., "05 - May"

                # Define the path based on organization preference
                type_folder = os.path.join(destination_folder, file_type.upper()) # Categorize by uppercase type
                year_folder = os.path.join(type_folder, year)

                if organize_by_month:
                    target_folder = os.path.join(year_folder, month)
                else:
                    target_folder = year_folder

                # Create the target directory if it doesn't exist
                os.makedirs(target_folder, exist_ok=True)

                # Move the file
                destination_path = os.path.join(target_folder, item)
                shutil.move(source_path, destination_path)
                print(f"Moved '{item}' to '{os.path.relpath(target_folder, destination_folder)}/{item}'")
                files_moved_count += 1

            except Exception as e:
                print(f"Error processing '{item}': {e}")
                errors_count += 1
        else:
            print(f"Skipping directory: '{item}'")

    print(f"\n--- Organization Complete ---")
    print(f"Successfully moved {files_moved_count} files.")
    if errors_count > 0:
        print(f"Encountered {errors_count} errors.")

def main():
    print("--- File Categorizer and Organizer App ---")
    source_folder = input("Enter the path to the folder containing files to organize: ")
    destination_folder = input("Enter the path for the destination folder where files will be categorized (e.g., 'Organized_Files'): ")

    choice = input("Organize files by month within each year? (yes/no, default: no): ").lower().strip()
    organize_by_month = (choice == 'yes' or choice == 'y')

    organize_files(source_folder, destination_folder, organize_by_month)

if __name__ == "__main__":
    main()