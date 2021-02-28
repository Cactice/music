"""
Download and install sverchok to blender.

This module downloads zipped sverchock module
and installs it.
"""
import requests

import bpy


def _download_url(url: str, save_path: str, chunk_size=128):
    req = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in req.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def _main():
    download_zip_file_path = "/usr/lib/master.zip"
    _download_url(
        "https://github.com/nortikin/sverchok/archive/master.zip",
        download_zip_file_path,
    )

    bpy.ops.preferences.addon_install(filepath=download_zip_file_path)
    bpy.ops.preferences.addon_enable(module="sverchok-master")
    bpy.ops.wm.save_userpref()


if __name__ == "__main__":
    _main()
