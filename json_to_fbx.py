"""
Converts a given json to glb file.

This file should be able to process both .blender and sverchok generated .json files
"""
import os
from time import sleep

import bpy
from sverchok.utils.logging import debug
from sverchok.utils.sv_json_import import JSONImporter

path = os.path


class _ExistingTreeError(Exception):
    """Exception raised for errors when Tree exists.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message=""):
        self.expression = expression
        self.message = message


def _prepare_bake_keyframe(act_frame):
    bpy.context.scene.frame_current = act_frame
    bpy.ops.node.sverchok_update_all()
    bpy.ops.object.join_shapes()
    bpy.context.object.active_shape_key_index = act_frame - 1


def _bake_frame(act_frame):
    _prepare_bake_keyframe(act_frame)
    active_object = bpy.context.active_object
    keys_name = active_object.data.shape_keys.name
    key = bpy.data.shape_keys[keys_name]
    key.key_blocks[-1].value = 1
    name = key.key_blocks[-1].name
    key.keyframe_insert(data_path=f'key_blocks["{name}"].value')
    key.key_blocks[-2].value = 0
    name_p = key.key_blocks[-2].name
    key.keyframe_insert(data_path=f'key_blocks["{name_p}"].value')
    bpy.context.scene.frame_current = act_frame - 1
    key.key_blocks[-1].value = 0
    key.keyframe_insert(data_path=f'key_blocks["{name}"].value')


def _bake_animation():
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
            but it can be created with another name (standard Blender's renaming)

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


def _main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    JSONImporter.init_from_path(
        path.join(current_dir, "sverchok/mechanical/ellipese-draw.json"),
    ).import_into_tree(_create_node_tree())
    # for bpy_obj in bpy.context.scene.objects:
    #     if bpy_obj.name in {"Light", "Camera"}:
    #         continue
    #     _bake_animation(bpy_obj)
    # bpy.ops.export_scene.gltf(filepath=path.join(current_dir, "lol.glb"))


if __name__ == "__main__":
    _main()
