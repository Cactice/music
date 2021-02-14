"""
Download and install sverchok to blender.

This module downloads zipped sverchock module
and installs it.
"""
import bpy
import requests


def download_url(url: str, save_path: str, chunk_size=128):
    """Download to a given path.

    Args:
        url (str): [description]
        save_path (str): [description]
        chunk_size (int, optional): [description]. Defaults to 128.
    """
    req = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in req.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


download_zip_file_path = "/usr/lib/master.zip"
download_url(
    "https://github.com/nortikin/sverchok/archive/master.zip",
    download_zip_file_path,
)

bpy.ops.preferences.addon_install(filepath=download_zip_file_path)
bpy.ops.preferences.addon_enable(module="sverchok-master")
bpy.ops.wm.save_userpref()
