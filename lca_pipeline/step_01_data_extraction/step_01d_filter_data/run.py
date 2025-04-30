from pathlib import Path
from methods.filter import load_yaml_config, load_json, save_json, filter_element_json, reorder_keys, filter_target_layer_json, reorder_keys_target_layer

def filter_data_sheets():

    # Paths Element
    yaml_path_element = Path("config/step_01_data_extraction/filter_element.yaml")
    element_input_dir = Path("data/pipeline/step_01_data_extraction/step_01c_dissect_layers/Elements")
    element_output_dir = Path("data/pipeline/step_01_data_extraction/step_01d_filter_data/Elements")

    # Paths Target Layer
    yaml_path_target_layer = Path("config/step_01_data_extraction/filter_target_layer.yaml")
    target_layer_input_dir = Path("data/pipeline/step_01_data_extraction/step_01c_dissect_layers/Target_Layers")
    target_layer_output_dir = Path("data/pipeline/step_01_data_extraction/step_01d_filter_data/Target_Layers")

    # Load filter config
    config_element = load_yaml_config(yaml_path_element)
    config_target_layer = load_yaml_config(yaml_path_target_layer)

    # Process element files
    for file_path in element_input_dir.glob("*.json"):
        try:
            data = load_json(file_path)
            filtered = filter_element_json(data, config_element)
            top_order = config_element.get("_top_level_order", [])
            if top_order:
                filtered = reorder_keys(filtered, top_order)
            save_json(filtered, element_output_dir / file_path.name)
        except Exception as e:
            continue

    # Process target layer files
    for file_path in target_layer_input_dir.glob("*.json"):
        try:
            data = load_json(file_path)
            filtered = filter_target_layer_json(data, config_target_layer)
            top_order = config_target_layer.get("_top_level_order", [])
            nested_order = config_target_layer.get("_building_element_context_order", [])
            # Reorder top-level
            if top_order:
                filtered = reorder_keys_target_layer(filtered, top_order)
            # Reorder second-level inside Building Element Context
            if "Building Element Context" in filtered and nested_order:
                filtered["Building Element Context"] = reorder_keys_target_layer(
                    filtered["Building Element Context"], nested_order
                )
            save_json(filtered, target_layer_output_dir / file_path.name)
        except Exception as e:
            continue

if __name__ == "__main__":
    filter_data_sheets()