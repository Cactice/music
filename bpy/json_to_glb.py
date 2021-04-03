"""
Converts a given json or .blender to glb file.

Execution Script:
blender -P json_to_glb.py -b --input_file=../sverchok/mechanical/ellipese-draw.json empty.blend

This file should be able to process both .blender and sverchok generated .json files
"""
import os
from pathlib import Path

import click
from sverchok.utils.logging import debug
from sverchok.utils.sv_json_import import JSONImporter

import bpy

path = os.path
current_dir = os.path.dirname(os.path.realpath(__file__))


class _ExistingTreeError(Exception):
    """Exception raised for errors when Tree exists.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message=""):
        self.expression = expression
        self.message = message


def _prepare_bake_keyframe(act_frame: int):
    bpy.context.scene.frame_current = act_frame
    bpy.ops.node.sverchok_update_all()
    bpy.ops.object.join_shapes()
    bpy.context.object.active_shape_key_index = act_frame - 1


def _bake_frame(act_frame: int):
    _prepare_bake_keyframe(act_frame)

    active_object = bpy.context.active_object
    keys_name = active_object.data.shape_keys.name
    key = bpy.data.shape_keys[keys_name]
    name = key.key_blocks[-1].name
    name_p = key.key_blocks[-2].name

    key.key_blocks[-1].value = 1
    key.keyframe_insert(data_path=f'key_blocks["{name}"].value')
    key.key_blocks[-2].value = 0
    key.keyframe_insert(data_path=f'key_blocks["{name_p}"].value')
    bpy.context.scene.frame_current = act_frame - 1
    key.key_blocks[-1].value = 0
    key.keyframe_insert(data_path=f'key_blocks["{name}"].value')


def _bake_animation(original_obj: bpy.types.Object):
    bpy.context.view_layer.objects.active = original_obj
    original_obj.select_set(True)
    original_name = bpy.context.active_object.name
    first_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end

    bpy.context.scene.frame_current = first_frame
    bpy.ops.node.sverchok_update_all()
    bpy.ops.object.duplicate()
    bpy.context.active_object.name = f"Baked_{original_name}"
    bpy.context.active_object.data.name = f"Baked_{original_name}"
    bpy.data.objects[original_name].select_set(state=True)
    bpy.ops.object.join_shapes()

    for act_frame in range(first_frame + 1, end_frame + 1):
        _bake_frame(act_frame)

    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = None


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


def _import_json(json_file):
    JSONImporter.init_from_path(json_file).import_into_tree(_create_node_tree())


@click.command(
    context_settings={
        "ignore_unknown_options": True,
    },
)
@click.option(
    "--input_file",
    type=click.Path(exists=True),
)
@click.argument("blender_args", nargs=-1, type=click.UNPROCESSED)
def _main(input_file, blender_args):
    extension = path.splitext(input_file)[1]
    file_name = path.splitext(path.basename(input_file))[0]
    if extension == ".json":
        _import_json(input_file)
    elif extension == ".blender":
        bpy.ops.wm.open_mainfile(filepath=input_file)

    # bake animation for all objs
    all_objs = bpy.context.scene.objects.items().copy()
    for name, each_obj in all_objs:
        if name in {"Light", "Camera", "Cube"}:
            continue
        _bake_animation(each_obj)

    bpy.ops.export_scene.gltf(
        filepath=path.join(current_dir, f"../next/public/glb/{file_name}.glb"),
    )


if __name__ == "__main__":
    _main()
