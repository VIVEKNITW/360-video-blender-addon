import bpy

def check_obj(obj):
    items_list = [item.name for item in list(bpy.data.objects)]
    if obj in items_list:
        return True
    else:
        return False


def deselect():
    bpy.ops.object.select_all(action='DESELECT')


def select_activate(object):
    object.select_set(True)
    bpy.context.view_layer.objects.active = object


def duplicate_items(my_list, joined):
    deselect()
    duplicate_list = []
    i = 1
    for item in my_list:
        select_activate(item)
        bpy.ops.object.duplicate_move()
        bpy.context.object.name = joined + str(i)
        duplicate_list.append(bpy.context.object)
        deselect()
        i+=1
    return duplicate_list


def join_items(duplicate_list, joined):
    deselect()
    for item in duplicate_list:
        select_activate(item)
                        
    bpy.ops.object.join()
    bpy.context.object.name = joined


def origin_to_gem(item):
    deselect()
    select_activate(item)
    bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')    


def add_empty(obj, joined):
    
    bpy.ops.object.empty_add(type='ARROWS')
    bpy.context.object.name = 'empty ' + joined
    return 'empty ' + joined


def make_child(my_list, empty):
    for item in my_list:
        select_activate(item)
        
    select_activate(empty)
    
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)


def emptytocenter(obj):
    deselect()
    select_activate(obj)
    bpy.ops.view3d.snap_cursor_to_center()
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)


def hide(object):
    bpy.context.view_layer.objects.active = object
    bpy.context.object.hide_set(True)


def unhide(object):
    bpy.context.view_layer.objects.active = object
    bpy.context.object.hide_set(False)


def white_background():
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
        
    for node in tree.nodes:
        tree.nodes.remove(node)
        
    my_node1 = tree.nodes.new(type = 'CompositorNodeRLayers')
    my_node1.location = 0,0
        
    my_node2 = tree.nodes.new(type = 'CompositorNodeAlphaOver')
    my_node2.location = 300,0
        
    my_node3 = tree.nodes.new(type = 'CompositorNodeComposite')
    my_node3.location = 500,0
        
    bpy.data.scenes["Scene"].node_tree.nodes["Alpha Over"].premul = 1

    links = tree.links
    link1 = links.new(my_node1.outputs[0], my_node2.inputs[2])
    link2 = links.new(my_node2.outputs[0], my_node3.inputs[0])
        
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.view_settings.view_transform = 'Standard'


def camera_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_perspective = 'CAMERA'
            break


def delete_obj(obj):
    deselect()
    select_activate(obj)
    bpy.ops.object.delete(use_global=False, confirm=False)


def makeparent(obj):
    deselect()
    bpy.data.objects[obj].select_set(True)
    bpy.data.objects['360_empty'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['360_empty']
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
    
    
def hidden_status():
    for obj in list(bpy.data.objects):
        if (obj.visible_get()):
            pass
        else:
            obj.hide_render = True    


def delete_extra_objects(initial_objects_list_name):
    del_objects = []
    all_objects = [item.name for item in list(bpy.data.objects)]
    for item in all_objects:
        if item not in initial_objects_list_name:
            del_objects.append(item)
    
        
    for obj in del_objects:
        try:
            unhide(bpy.data.objects[obj])
            select_activate(bpy.data.objects[obj])
            bpy.ops.object.delete()
        except:
            pass