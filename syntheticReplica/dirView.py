# AUTOGENERATED! DO NOT EDIT! File to edit: 03_dirView.ipynb (unless otherwise specified).

__all__ = ['mkDir', 'additionalMssg', 'fileCount', 'listFile', 'itemize', 'rmFile', 'rmFileExt', 'rmDir', 'showDirInf']

# Cell
from pathlib import Path
import random
import shutil

# Cell
# Make dir, parents=True, exist_ok=True
def mkDir(base_path:Path, dir_list:list) -> None:
    path_names = []
    for name in dir_list:
        name = (base_path).joinpath(name)
        name.mkdir(parents=True, exist_ok=True)
        path_names.append(name)


# Cell
# Display additional message
def additionalMssg(count:int) -> None:
    if count == 0:
        print("All images are ready to display, please proceed!")
    elif count > 0:
        print(f'Not a JPG or PNG files: {count}')

# Cell
# Count total quantity of files
def fileCount(path_dir:Path) -> int:
    dir_size = len(list(path_dir.iterdir()))
    print(f'Total number of items found: {dir_size}')
    return dir_size

# Cell
# List path to subdirs or paths to files of a dir
def listFile(path_dir:Path) -> list:
    return sorted(list(path_dir.iterdir()))

# Cell
# Enumerate list of file names and paths
def itemize(path_dir:Path) -> list:
    return [i for i in enumerate(listFile(path_dir))]

# Cell
# Remove file with name and extension
def rmFile(id:list, path_dir:Path) -> None:
    itemize(path_dir)
    # Remove paths corresponding to id in the list.
    list(map(lambda x: (itemize(path_dir)[x][1]).unlink(), id))

# Cell
# Remove all files with a specific extension in a directory
def rmFileExt(path_dir:Path, extension:str) -> None:
    enum = itemize(path_dir)
    for i in range(len(enum)):
        _, path = enum[i]
        if path.is_file() and path.suffix == extension:
            path.unlink()
            print(f'"{path}"" removed!')

    print(f'All "{extension}" removed!')

# Cell

# Remove directory or subdirectory
def rmDir(path_dir:Path, dir:str) -> None:
    dir_list = listFile(path_dir)
    folder = path_dir.joinpath(dir)
    if folder in dir_list:
        shutil.rmtree(folder)
        print(f'"{folder}"" removed' )

# Cell
# Display image file information within a directory
def showDirInf(path_dir:Path, suffix_list:list = ['.jpg', '.jpeg', '.png']) -> None:
    count = 0
    enum = itemize(path_dir)
    for i in range(len(enum)):
        id, path = enum[i]
        if path.suffix not in suffix_list:
            print(f'{id}: Not a JPG or PNG, please remove before proceeding -> {path.name}')
            count += 1
        else:
            print(f'{id}: {path.name}')

    print(f'\nPath to files: "{path.parents[0]}"')
    fileCount(path_dir)
    additionalMssg(count)