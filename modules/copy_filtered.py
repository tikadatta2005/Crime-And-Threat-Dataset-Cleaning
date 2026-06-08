import os
import shutil
import uuid
import random


def copy_filtered(
    input_dir,
    output_dir,
    includes=None,
    excludes=None,
    skip=None,
    seed=None
):
    """
    Copies files from input_dir to output_dir with optional filtering.

    Parameters
    ----------
    input_dir : str
        Source directory.

    output_dir : str
        Destination directory.

    includes : list[str] | None
        Copy only files whose names contain ANY of these strings
        (case-insensitive).

    excludes : list[str] | None
        Skip files whose names contain ANY of these strings
        (case-insensitive).

    skip : int | None
        If provided, divides files into chunks of size `skip`
        and randomly selects 1 file from each chunk.

        Example:
            skip=5
            100 files -> ~20 copied files

    seed : int | None
        Random seed for reproducibility.
    """

    if seed is not None:
        random.seed(seed)

    os.makedirs(output_dir, exist_ok=True)

    includes = [x.lower() for x in includes] if includes else None
    excludes = [x.lower() for x in excludes] if excludes else None

    unique_tag = str(uuid.uuid4())[:8]

    files = sorted(
        f for f in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, f))
    )

    # Apply include/exclude filtering first
    filtered_files = []

    for filename in files:
        lower_name = filename.lower()

        if includes and not any(x in lower_name for x in includes):
            continue

        if excludes and any(x in lower_name for x in excludes):
            continue

        filtered_files.append(filename)

    # Random sampling by chunks
    if skip and skip > 1:
        selected_files = []

        for start in range(0, len(filtered_files), skip):
            chunk = filtered_files[start:start + skip]

            if chunk:
                selected_files.append(random.choice(chunk))
    else:
        selected_files = filtered_files

    copied = 0

    for filename in selected_files:
        src_path = os.path.join(input_dir, filename)

        name, ext = os.path.splitext(filename)
        new_name = f"{name}_{unique_tag}{ext}"

        dst_path = os.path.join(output_dir, new_name)

        shutil.copy2(src_path, dst_path)
        copied += 1

    print(
        f"Copied {copied}/{len(filtered_files)} filtered files "
        f"to '{output_dir}'"
    )