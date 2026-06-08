import os
import shutil
import uuid

def copy_filtered(input_dir, output_dir, includes=None, excludes=None):
    """
    Copies files from input_dir to output_dir with optional include/exclude filters.
    
    Rules:
    - If includes is provided, only files containing any include string (case-insensitive) are copied.
    - If excludes is provided, files containing any exclude string (case-insensitive) are skipped.
    - A unique suffix is added to each copied file name to avoid collisions.
    """

    os.makedirs(output_dir, exist_ok=True)

    includes = [i.lower() for i in includes] if includes else None
    excludes = [e.lower() for e in excludes] if excludes else None

    unique_tag = str(uuid.uuid4())[:8]

    for filename in os.listdir(input_dir):
        src_path = os.path.join(input_dir, filename)

        if not os.path.isfile(src_path):
            continue

        lower_name = filename.lower()

        # include filter
        if includes:
            if not any(i in lower_name for i in includes):
                continue

        # exclude filter
        if excludes:
            if any(e in lower_name for e in excludes):
                continue

        name, ext = os.path.splitext(filename)
        new_name = f"{name}_{unique_tag}{ext}"
        dst_path = os.path.join(output_dir, new_name)

        shutil.copy2(src_path, dst_path)