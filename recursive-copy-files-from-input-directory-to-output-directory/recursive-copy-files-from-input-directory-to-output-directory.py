# File Copying Script
#
# Description:
# This script recursively traverses a specified input directory, finds all files
# within it (including those in subfolders), and copies them to a specified
# output directory. The original folder structure is not preserved in the output;
# all files are placed directly into the root of the output directory.
#
# If a file with the same name already exists in the output directory, it will be
# overwritten, and a warning will be displayed.
#
# Required Libraries:
# This script uses standard Python libraries (os, shutil, argparse) and does not
# require any external packages to be installed.
#
# Usage from the terminal:
# python copy_files.py -input "/path/to/source_folder" -output "/path/to/destination_folder"

import os
import shutil
import argparse

def copy_all_files(input_dir, output_dir):
    """
    Recursively finds all files in the input directory and copies them to the
    output directory.

    Args:
        input_dir (str): The full path to the source directory.
        output_dir (str): The full path to the destination directory.
    """
    # Create the output directory if it doesn't already exist.
    # The `exist_ok=True` argument prevents an error if the directory is already there.
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create output directory '{output_dir}'. Reason: {e}")
        return

    print(f"Scanning '{input_dir}' for files...")
    file_count = 0

    # os.walk() generates the file names in a directory tree by walking the tree
    # either top-down or bottom-up.
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            # Construct the full path of the source file
            source_path = os.path.join(root, filename)
            
            # Construct the full path of the destination file
            destination_path = os.path.join(output_dir, filename)

            # Check if a file with the same name already exists in the destination
            if os.path.exists(destination_path):
                print(f"Warning: Overwriting existing file: {destination_path}")

            try:
                # shutil.copy2 attempts to preserve file metadata (like timestamps)
                shutil.copy2(source_path, destination_path)
                print(f"Copied: {filename} -> {output_dir}")
                file_count += 1
            except Exception as e:
                print(f"Error: Could not copy file {source_path}. Reason: {e}")
    
    print(f"\nProcess complete. Copied {file_count} files.")


def main():
    """
    Parses command-line arguments and initiates the file copying process.
    """
    parser = argparse.ArgumentParser(
        description="Recursively find and copy all files from an input directory to an output directory."
    )

    parser.add_argument(
        "-input",
        required=True,
        help="The full path to the source directory containing the files."
    )
    parser.add_argument(
        "-output",
        required=True,
        help="The full path to the destination directory where files will be copied."
    )

    args = parser.parse_args()

    # Normalize paths to handle different OS path formats (e.g., slashes vs. backslashes)
    input_directory = os.path.normpath(args.input)
    output_directory = os.path.normpath(args.output)

    # Check if the input directory exists and is actually a directory
    if not os.path.isdir(input_directory):
        print(f"Error: The input directory '{input_directory}' does not exist or is not a directory.")
        return
        
    copy_all_files(input_directory, output_directory)


if __name__ == "__main__":
    main()
