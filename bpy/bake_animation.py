"""Bakes animation between given first and last frame."""
import os
from pathlib import Path

import click
from sverchok.utils.logging import debug
from sverchok.utils.sv_json_import import JSONImporter

import bpy


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


def bake_animation(original_obj: bpy.types.Object, first_frame: int, last_frame: int):
    """Bakes animation between given first and last frame.

    Args:
        original_obj (bpy.types.Object): Object to bake
        first_frame (int): First frame
        last_frame (int): Last Frame
    """
    bpy.context.view_layer.objects.active = original_obj
    original_obj.select_set(True)
    original_name = bpy.context.active_object.name

    bpy.context.scene.frame_current = first_frame
    bpy.ops.node.sverchok_update_all()
    bpy.ops.object.duplicate()
    bpy.context.active_object.name = f"Baked_{original_name}"
    bpy.context.active_object.data.name = f"Baked_{original_name}"
    bpy.data.objects[original_name].select_set(state=True)
    bpy.ops.object.join_shapes()

    for act_frame in range(first_frame + 1, last_frame + 1):
        _bake_frame(act_frame)

    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = None
