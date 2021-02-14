"""
Converts a given json to glb file.

This file should be able to process both .blender and sverchok generated .json files
"""
import bpy
from sverchok.utils.logging import debug
from sverchok.utils.sv_json_import import JSONImporter


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
    scene = bpy.context.scene
    scene.frame_current = act_frame
    bpy.ops.node.sverchok_update_all()
    bpy.ops.object.join_shapes()


def _bake_frame(act_frame):
    _prepare_bake_keyframe(act_frame)
    bpy_obj = bpy.context.object
    bpy_obj.active_shape_key_index = act_frame - 1
    keys_name = bpy_obj.data.shape_keys.name
    key = bpy.data.shape_keys[keys_name]
    name = key.key_blocks[-2].name
    key.key_blocks[-1].value = 1
    key.keyframe_insert(
        data_path=f"key_blocks['{name}'].value",
    )
    key.key_blocks[-3].value = 0
    name_p = key.key_blocks[-3].name
    key.keyframe_insert(
        data_path=f"key_blocks['{name_p}'].value",
    )
    bpy.context.scene.frame_current = act_frame
    key.key_blocks[-2].value = 0
    key.keyframe_insert(
        data_path=f"key_blocks['{name_p}'].value",
    )


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


JSONImporter.init_from_path(
    "/home/yuya/git/blender-sverchok-practice/sverchok/mechanical/gear.json",
).import_into_tree(_create_node_tree())
