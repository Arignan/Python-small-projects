import os
import re
import datetime

def get_files_in_folder(folder_path):
    """Returns a list of file paths in the given folder."""
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return []
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def rename_files_sequentially(files, base_name="file", start_num=1, padding=3):
    """Renames files sequentially (e.g., file_001.txt, file_002.txt)."""
    renamed_count = 0
    for i, old_path in enumerate(files):
        directory, old_filename = os.path.split(old_path)
        _, ext = os.path.splitext(old_filename)
        new_filename = f"{base_name}_{str(start_num + i).zfill(padding)}{ext}"
        new_path = os.path.join(directory, new_filename)
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: '{old_filename}' to '{new_filename}'")
            renamed_count += 1
        except OSError as e:
            print(f"Error renaming '{old_filename}': {e}")
    return renamed_count

def rename_files_with_pattern(files, pattern_format, start_index=1):
    """Renames files using a custom pattern (e.g., Image_001.jpg, Doc_A_001.pdf).
    Pattern format can use {index}, {original_name}, {ext}, {date}.
    """
    renamed_count = 0
    for i, old_path in enumerate(files):
        directory, old_filename = os.path.split(old_path)
        base_name, ext = os.path.splitext(old_filename)

        # Replace placeholders in the pattern
        new_filename_base = pattern_format.format(
            index=str(start_index + i).zfill(3), # Default padding for index
            original_name=base_name,
            ext=ext,
            date=datetime.date.today().strftime("%Y%m%d")
        )
        new_filename = f"{new_filename_base}{ext}" # Ensure extension is added back
        new_path = os.path.join(directory, new_filename)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: '{old_filename}' to '{new_filename}'")
            renamed_count += 1
        except OSError as e:
            print(f"Error renaming '{old_filename}': {e}")
    return renamed_count

def rename_files_by_date(files, date_format="%Y%m%d", base_name="file", start_num=1, padding=3):
    """Renames files with a date prefix (e.g., 20250526_file_001.txt)."""
    renamed_count = 0
    current_date_str = datetime.date.today().strftime(date_format)
    for i, old_path in enumerate(files):
        directory, old_filename = os.path.split(old_path)
        _, ext = os.path.splitext(old_filename)
        new_filename = f"{current_date_str}_{base_name}_{str(start_num + i).zfill(padding)}{ext}"
        new_path = os.path.join(directory, new_filename)
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: '{old_filename}' to '{new_filename}'")
            renamed_count += 1
        except OSError as e:
            print(f"Error renaming '{old_filename}': {e}")
    return renamed_count

def main():
    print("--- File Renamer App ---")
    folder_path = input("Enter the path to the folder you want to scan: ")

    files_to_rename = get_files_in_folder(folder_path)

    if not files_to_rename:
        print("No files found in the specified folder or folder does not exist. Exiting.")
        return

    print(f"\nFound {len(files_to_rename)} files in '{folder_path}'.")
    print("Choose a renaming style:")
    print("1. Continuous numbering (e.g., file_001.txt, file_002.txt)")
    print("2. Custom pattern (e.g., Photo_{index}.jpg, Report_{date}_{original_name}.pdf)")
    print("3. Date prefix with numbering (e.g., 20250526_file_001.txt)")
    
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        base_name = input("Enter the base name for files (e.g., 'document'): ") or "file"
        try:
            start_num = int(input("Enter the starting number (default: 1): ") or "1")
            padding = int(input("Enter padding for numbers (e.g., 3 for 001, default: 3): ") or "3")
        except ValueError:
            print("Invalid number entered. Using defaults (start=1, padding=3).")
            start_num = 1
            padding = 3
        
        print("\n--- Initiating Sequential Renaming ---")
        renamed_count = rename_files_sequentially(files_to_rename, base_name, start_num, padding)
        print(f"\nSuccessfully renamed {renamed_count} files.")

    elif choice == '2':
        print("\n--- Custom Pattern Renaming ---")
        print("Available placeholders: {index} (sequential number), {original_name}, {ext} (original extension), {date} (YYYYMMDD)")
        pattern_format = input("Enter your custom pattern (e.g., 'MyPhoto_{index}', 'Report_{date}_{original_name}'): ")
        try:
            start_index = int(input("Enter the starting index for {index} (default: 1): ") or "1")
        except ValueError:
            print("Invalid number entered. Using default (start=1).")
            start_index = 1

        if not pattern_format:
            print("No pattern entered. Exiting.")
            return

        print("\n--- Initiating Custom Pattern Renaming ---")
        renamed_count = rename_files_with_pattern(files_to_rename, pattern_format, start_index)
        print(f"\nSuccessfully renamed {renamed_count} files.")

    elif choice == '3':
        print("\n--- Date Prefix Renaming ---")
        date_format_input = input("Enter date format (e.g., %Y%m%d for 20250526, %Y-%m-%d for 2025-05-26, default: %Y%m%d): ") or "%Y%m%d"
        base_name = input("Enter the base name for files (e.g., 'scan'): ") or "file"
        try:
            start_num = int(input("Enter the starting number (default: 1): ") or "1")
            padding = int(input("Enter padding for numbers (e.g., 3 for 001, default: 3): ") or "3")
        except ValueError:
            print("Invalid number entered. Using defaults (start=1, padding=3).")
            start_num = 1
            padding = 3

        print("\n--- Initiating Date Prefix Renaming ---")
        renamed_count = rename_files_by_date(files_to_rename, date_format_input, base_name, start_num, padding)
        print(f"\nSuccessfully renamed {renamed_count} files.")

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()