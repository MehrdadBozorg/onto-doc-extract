
from pathlib import Path
import os 
from src.transformer import read_pdf
def test():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory
    parent_dir = Path(os.path.dirname(current_dir)).parent.parent

    # Define the target directory inside the parent directory
    target_dir = os.path.join(parent_dir, "samples")

    # Define the file path
    file_path = Path(target_dir) / "sample.pdf"
    print(read_pdf(file_path))