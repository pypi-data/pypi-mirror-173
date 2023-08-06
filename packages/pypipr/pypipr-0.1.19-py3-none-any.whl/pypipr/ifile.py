IFILE = True

"""PYPIPR Module"""


"""PYTHON Standard Module"""
from pathlib import Path


"""PYPI Module"""


def file_get_contents(filename):
    """
    Membaca seluruh isi file ke memory.
    Apabila file tidak ada maka akan return None.
    Apabila file ada tetapi kosong, maka akan return empty string
    """
    try:
        f = open(filename, "r")
        r = f.read()
        f.close()
        return r
    except:
        return None


def file_put_contents(filename, contents):
    """
    Menuliskan content ke file.
    Apabila file tidak ada maka file akan dibuat.
    Apabila file sudah memiliki content maka akan di overwrite.
    """
    f = open(filename, "w")
    r = f.write(contents)
    f.close()
    return r


def create_folder(folder_name):
    """
    Membuat folder.
    Membuat folder secara recursive dengan permission.
    """
    Path(folder_name).mkdir(parents=True, exist_ok=True)


def scan_folder(folder_name, recursive=True):
    """
    Hanya mengumpulkan nama-nama folder dan subfolder.
    Tidak termasuk [".", ".."].
    """
    pass


def scan_file(folder_name, recursive=True):
    """
    Hanya mengumpulkan nama-nama file dalam folder dan subfolder.
    """
    pass
