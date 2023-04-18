"""Categorize PDFs according to the tree structure in JSON."""
import json
import os
import shutil


ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pub-adp-r2211")
JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pub-adp-r2211.json")
SOURCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "adp-r2211_pdfs")

def cat_pdfs(source_pdfs, json_path):
    """Categorize PDFs according to the tree structure in JSON.
        
        :param source_pdfs: Directory containing PDFs.
        :param json_path: Path to JSON file containing the tree structure.
        :return: None.
    """
    # read JSON file
    with open(json_path, 'r') as f:
        json_objs = json.load(f)

    # flatten JSON tree and create target_pdf_paths
    target_pdf_paths = []
    for type, objs in json_objs.items():
        pdf_path_lv1 = os.path.join(ROOT_DIR, type)
        for arch_element, pdfs in objs.items():
            pdf_path = os.path.join(pdf_path_lv1, arch_element)
            for pdf in pdfs:
                target_pdf_paths.append(os.path.join(pdf_path, pdf))
                
    
    # list each pdf paths in source_pdf_paths
    source_pdf_paths = []
    for root, dirs, files in os.walk(source_pdfs):
        for file in files:
            if file.endswith(".pdf"):
                source_pdf_paths.append(os.path.join(root, file))

    # map source_pdf_paths to target_pdf_paths according their pdf file names
    mappings = {}
    for pdf_path in source_pdf_paths:
        pdf_name = os.path.basename(pdf_path)
        for target_pdf_path in target_pdf_paths:
            target_pdf_name = os.path.basename(target_pdf_path)
            if pdf_name == target_pdf_name:
                mappings[pdf_path] = target_pdf_path
        
    for mapping in mappings:
        if not os.path.exists(os.path.dirname(mappings[mapping])):
            os.makedirs(os.path.dirname(mappings[mapping]))
        # copy file to target directory
        shutil.copyfile(mapping, mappings[mapping])

    pass


if __name__ == "__main__":
    cat_pdfs(SOURCE_PATH, JSON_PATH)