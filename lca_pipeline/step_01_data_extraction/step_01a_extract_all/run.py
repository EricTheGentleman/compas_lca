import time
from pathlib import Path
from methods.extractor import extractor
from methods.helpers_io import load_ifc_file, load_extraction_config, get_single_ifc_file

def extract_all():

    start_time = time.time()

    # Input, output and config paths
    input_file = str(get_single_ifc_file())
    out_directory_compositions = Path("data/pipeline/step_01_data_extraction/step_01a_extract_all/Compositions")
    out_directory_elements = Path("data/pipeline/step_01_data_extraction/step_01a_extract_all/Elements")
    out_directory_boq = Path("data/pipeline/step_01_data_extraction/step_01a_extract_all")
    config_path = Path("config/step_01_data_extraction/extraction_config.yaml")

    # Specify max_objects that should be counted. Enter "None" to process all objects.
    max_objects = None

    # Load the extraction configuration from a YAML file
    config = load_extraction_config(config_path)

    try:
        # Load the IFC file
        model = load_ifc_file(input_file)

        # Extract element data and save each IfcBuildingElement separately
        extractor(input_file, model, out_directory_elements, out_directory_compositions, out_directory_boq, max_objects, config)

        # Stop measuring time
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"All elements extracted in {elapsed_time:.2f} seconds.")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    extract_all()