import os
import shutil
import uuid


def copy_to_label_dir(filename, input_dir, output_dir, label):
    """
    Copies:
        input_dir/filename
    To:
        output_dir/label/unique_filename
    """

    src_path = os.path.join(input_dir, filename)

    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"File not found: {src_path}")

    label_dir = os.path.join(output_dir, label)
    os.makedirs(label_dir, exist_ok=True)

    name, ext = os.path.splitext(filename)
    unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"

    dst_path = os.path.join(label_dir, unique_name)

    shutil.copy2(src_path, dst_path)

    print(f"File moved to: {dst_path}")