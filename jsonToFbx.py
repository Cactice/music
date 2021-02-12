from sverchok.utils.sv_json_import import JSONImporter
import bpy


def bake_animation():
    original_name = bpy.context.active_object.name
    first_frame = bpy.context.scene.frame_start 
    end_frame = bpy.context.scene.frame_end 
    bpy.context.scene.frame_current = first_frame
    bpy.ops.node.sverchok_update_all()
    bpy.ops.object.duplicate()
    bpy.context.active_object.name = 'Baked_' + original_name
    bpy.context.active_object.data.name = 'Baked_' + original_name
    bpy.data.objects[original_name].select_set(state=True)
    bpy.ops.object.join_shapes()
    for actFrame in range(first_frame+1, end_frame+1):
        bpy.context.scene.frame_current = actFrame
        bpy.ops.node.sverchok_update_all()
        bpy.ops.object.join_shapes()
        bpy.context.object.active_shape_key_index = actFrame-1
        keys_name = bpy.context.object.data.shape_keys.name
        k = bpy.data.shape_keys[keys_name]
        k.key_blocks[-1].value = 1
        name = bpy.data.shape_keys[keys_name].key_blocks[-1].name
        bpy.data.shape_keys[keys_name].keyframe_insert(data_path='key_blocks["'+ name +'"].value')
        k.key_blocks[-2].value = 0
        name_p = bpy.data.shape_keys[keys_name].key_blocks[-2].name
        bpy.data.shape_keys[keys_name].keyframe_insert(data_path='key_blocks["'+ name_p +'"].value')
        bpy.context.scene.frame_current = actFrame-1
        k.key_blocks[-1].value = 0
        bpy.data.shape_keys[keys_name].keyframe_insert(data_path='key_blocks["'+ name +'"].value')
    bpy.data.shape_keys[keys_name].(null) = "Animation"

def create_node_tree(name=None, must_not_exist=True):
    """
    Create new Sverchok node tree in the scene.
    If must_not_exist == True (default), then it is checked that
    the tree with such name did not exist before. If it exists,
    an exception is raised.
    If must_not_exist == False, then new tree will be created anyway,
    but it can be created with another name (standard Blender's renaming).
    """
    if name is None:
        name = "TestingTree"
    if must_not_exist:
        if name in bpy.data.node_groups:
            raise Exception("Will not create tree `{}': it already exists".format(name))
    debug("Creating tree: %s", name)
    return bpy.data.node_groups.new(name=name, type="SverchCustomTreeType")
    
JSONImporter
.init_from_path('/home/yuya/git/blender-sverchok-practice/mechanical/gear.json')
.import_into_tree(create_node_tree())