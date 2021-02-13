import bpy
import requests


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


download_zip_file_path = "/usr/lib/master.zip"
download_url(
    "https://github.com/nortikin/sverchok/archive/master.zip", download_zip_file_path
)

bpy.ops.preferences.addon_install(filepath=download_zip_file_path)
bpy.ops.preferences.addon_enable(module="sverchok-master")
bpy.ops.wm.save_userpref()
