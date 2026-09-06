# PDF Rotator Script
#
# Description:
# This script recursively finds all PDF files in a specified directory and rotates
# each page by a given degree (90, 180, or 270). The rotation can be set to
# either counter-clockwise (default) or clockwise. The original files are
# replaced with their rotated versions.
#
# Required Library:
# You must install PyPDF2 for this script to work.
# pip install PyPDF2
#
# Usage from the terminal:
# python rotate_pdfs.py -directory "/path/to/your/folder" -degree 90
#
# To rotate clockwise:
# python rotate_pdfs.py -directory "/path/to/your/folder" -degree 90 -negsign

import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def rotate_pdf_file(file_path, rotation_angle):
    """
    Rotates every page in a single PDF file and overwrites the original.

    Args:
        file_path (str): The full path to the PDF file.
        rotation_angle (int): The angle to rotate by. Positive for
                              counter-clockwise, negative for clockwise.
    """
    try:
        # Open the existing PDF
        reader = PdfReader(file_path)
        writer = PdfWriter()

        # Rotate each page and add it to the writer object
        for page in reader.pages:
            # The rotate() method rotates counter-clockwise for positive angles
            page.rotate(rotation_angle)
            writer.add_page(page)

        # Overwrite the original file with the rotated content
        with open(file_path, "wb") as output_pdf:
            writer.write(output_pdf)
        
        print(f"Successfully rotated: {file_path}")

    except Exception as e:
        print(f"Could not process file {file_path}. Error: {e}")


def main():
    """
    Parses command-line arguments and initiates the PDF search and rotation process.
    """
    parser = argparse.ArgumentParser(
        description="Recursively find and rotate all PDF files in a directory."
    )

    parser.add_argument(
        "-directory",
        required=True,
        help="The full path to the directory to search for PDFs."
    )
    parser.add_argument(
        "-degree",
        required=True,
        type=int,
        choices=[90, 180, 270],
        help="The degree of rotation. Must be 90, 180, or 270."
    )
    parser.add_argument(
        "-negsign",
        action="store_true", # Makes this a flag; stores True if present
        help="Use this flag to rotate clockwise. Default is counter-clockwise."
    )

    args = parser.parse_args()

    # Normalize the path to remove any trailing slashes or backslashes
    target_directory = os.path.normpath(args.directory)
    degree = args.degree
    is_clockwise = args.negsign

    # Check if the provided directory exists
    if not os.path.isdir(target_directory):
        print(f"Error: The directory '{target_directory}' does not exist.")
        return

    # Determine the final angle for the PyPDF2 library.
    # Positive angles rotate counter-clockwise, negative angles rotate clockwise.
    final_rotation_angle = -degree if is_clockwise else degree

    direction = "clockwise" if is_clockwise else "counter-clockwise"
    print(f"Starting PDF scan in: '{target_directory}'")
    print(f"Rotation will be {degree}° {direction}.\n")

    # os.walk() travels through the directory tree top-down
    for root, dirs, files in os.walk(target_directory):
        for filename in files:
            # Check for .pdf extension (case-insensitive)
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(root, filename)
                rotate_pdf_file(file_path, final_rotation_angle)

    print("\nPDF rotation process completed.")

if __name__ == "__main__":
    main()

