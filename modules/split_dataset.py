import os
import random
import shutil
from pathlib import Path

def split_dataset(input_dir, output_dir, seed=42):
    """
    Splits dataset into train/val/test with 70/15/15 ratio.

    Structure assumed:
        input_dir/
            class1/
            class2/
            ...

    Output:
        output_dir/
            train/class1
            val/class1
            test/class1
            ...
    """
    random.seed(seed)

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    splits = {
        "train": 0.7,
        "val": 0.15,
        "test": 0.15
    }

    # create base folders
    for split in splits:
        (output_dir / split).mkdir(parents=True, exist_ok=True)

    # iterate class folders
    for class_dir in input_dir.iterdir():
        if not class_dir.is_dir():
            continue

        class_name = class_dir.name
        files = [f for f in class_dir.iterdir() if f.is_file()]

        random.shuffle(files)

        n = len(files)
        train_end = int(n * splits["train"])
        val_end = train_end + int(n * splits["val"])

        split_map = {
            "train": files[:train_end],
            "val": files[train_end:val_end],
            "test": files[val_end:]
        }

        for split_name, split_files in split_map.items():
            out_class_dir = output_dir / split_name / class_name
            out_class_dir.mkdir(parents=True, exist_ok=True)

            for f in split_files:
                shutil.copy2(f, out_class_dir / f.name)

    return str(output_dir)