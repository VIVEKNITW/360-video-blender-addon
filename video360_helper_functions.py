import bpy

def deselect():
    bpy.ops.object.select_all(action='DESELECT')
    
    
def hide(object):
    bpy.context.view_layer.objects.active = object
    bpy.context.object.hide_set(True)
    
def unhide(object):
    bpy.context.view_layer.objects.active = object
    bpy.context.object.hide_set(False)
        
        
def select_activate(object):
    object.select_set(True)
    bpy.context.view_layer.objects.active = object


def origin_to_gem(item):
    deselect()
    select_activate(item)
    bpy.ops.object.origin_set(type = 'ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')    
    

def duplicate_items(my_list):
    duplicate_list = []
    for item in my_list:
        select_activate(item)
        bpy.ops.object.duplicate_move()
        duplicate_list.append(bpy.context.object)
        deselect()
    return duplicate_list


def join_items(duplicate_list):
    for item in duplicate_list:
        select_activate(item)
                        
    bpy.ops.object.join()
    bpy.context.object.name = 'joined'
    

def obj_to_org(obj):
    
    bpy.ops.object.empty_add(type='ARROWS')
    bpy.context.object.name = 'empty_parent'


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
    
    
def makeparent():
    deselect()
    bpy.data.objects['empty_parent'].select_set(True)
    bpy.data.objects['360_empty'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['360_empty']
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
    

def hidden_status():
    for obj in list(bpy.data.objects):
        if (obj.visible_get()):
            pass
        else:
            obj.hide_render = True

def camera_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_perspective = 'CAMERA'
            break