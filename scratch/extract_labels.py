import onnxruntime as ort
import json

def extract_labels(model_path):
    try:
        session = ort.InferenceSession(model_path)
        metadata = session.get_modelmeta().custom_metadata_map
        if 'names' in metadata:
            names = metadata['names']
            # Ultralytics names are usually a JSON string or a dict represented as string
            # Format: "{0: 'person', 1: 'bicycle', ...}" or similar
            try:
                # Try to parse as JSON first (though it's often not valid JSON)
                labels_dict = json.loads(names.replace("'", '"'))
                labels = [labels_dict[str(i)] for i in range(len(labels_dict))]
                return labels
            except:
                # Fallback: manual parsing
                import ast
                labels_dict = ast.literal_eval(names)
                labels = [labels_dict[i] for i in range(len(labels_dict))]
                return labels
    except Exception as e:
        print(f"Error extracting labels: {e}")
    return None

if __name__ == "__main__":
    labels = extract_labels(r"d:\LPV\server\onnx_model\yolo26s.onnx")
    if labels:
        print("\n".join(labels))
    else:
        print("No labels found in metadata.")
