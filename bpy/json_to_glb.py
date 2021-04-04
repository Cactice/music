"""
Converts a given json or .blender to glb file.

Execution Script:
blender -P json_to_glb.py -b --input_dir=../sverchok/ empty.blend


This file should be able to process both .blender and sverchok generated .json files
"""
import os
import sys
from glob import glob
from pathlib import Path

import click
from sverchok.utils.logging import debug
from sverchok.utils.sv_json_import import JSONImporter

import bpy

path = os.path
current_dir = os.path.dirname(os.path.realpath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from bake_animation import bake_animation  # noqa: E402


class _ExistingTreeError(Exception):
    """Exception raised for errors when Tree exists.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message=""):
        self.expression = expression
        self.message = message


def _create_node_tree(
    name="TestingTree",
    must_not_exist=True,
) -> bpy.types.BlendDataNodeTrees:
    """
    Create new Sverchok node tree in the scene.

    Description: hello

    Args:
        name (str, optional): Defaults to "TestingTree"
        must_not_exist (bool, optional): Defaults to True.

            If must_not_exist == True (default), then it is checked that
            the tree with such name did not exist before. If it exists,
            an exception is raised.
            If must_not_exist == False, then new tree will be created anyway,
            but it can be created with another name
            (standard Blender's renaming)

    Raises:
        _ExistingTreeError: Tree name already existed

    Returns:
        bpy.BlendDataNodeTrees: Created nodeTree
    """
    if must_not_exist:
        if name in bpy.data.node_groups:
            raise _ExistingTreeError(
                f"Will not create tree `{name}': it already exists",
            )
    debug(f"Creating tree: {name}")
    return bpy.data.node_groups.new(name=name, type="SverchCustomTreeType")


def _select_baked():
    all_objs = bpy.context.scene.objects.items().copy()
    bpy.ops.object.select_all(action="DESELECT")
    for name, _each_obj in all_objs:
        if name.startswith("Baked_"):
            bpy.data.objects[name].select_set(True)


def _import_json(json_file):
    JSONImporter.init_from_path(json_file).import_into_tree(_create_node_tree())


def _export_file(input_file):
    first_frame = 0
    last_frame = 100
    bpy.ops.wm.read_homefile(use_empty=True)
    extension = path.splitext(input_file)[1]
    file_dir = path.dirname(input_file).split("/sverchok/")[1]
    file_name = path.splitext(path.basename(input_file))[0]
    if extension == ".json":
        _import_json(input_file)
    elif extension == ".blender":
        bpy.ops.wm.open_mainfile(filepath=input_file)
        first_frame = bpy.context.scene.frame_start
        last_frame = bpy.context.scene.frame_end

    # bake animation for all objs
    all_objs = bpy.context.scene.objects.items().copy()
    for name, each_obj in all_objs:
        if name not in {"Light", "Camera", "Cube"}:
            bake_animation(each_obj, first_frame, last_frame)
    _select_baked()

    os.makedirs(
        path.join(current_dir, f"../next/public/glb/{file_dir}"),
        exist_ok=True,
    )
    bpy.ops.export_scene.gltf(
        filepath=path.join(
            current_dir,
            f"../next/public/glb/{file_dir}/{file_name}.glb",
        ),
        export_selected=True,
    )


@click.command(
    context_settings={
        "ignore_unknown_options": True,
    },
)
@click.option("--input_dir", type=click.Path(exists=True))
@click.argument("blender_args", nargs=-1, type=click.UNPROCESSED)
def _main(input_dir, blender_args):
    original_files = glob(
        path.join(current_dir, input_dir, "**/*.json"),
        recursive=True,
    ) + glob(
        path.join(current_dir, input_dir, "**/*.blender"),
        recursive=True,
    )

    for original_file in original_files:
        _export_file(original_file)


if __name__ == "__main__":
    _main()
