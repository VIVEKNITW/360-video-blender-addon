import bpy, math
from .video360_helper_functions import check_obj, duplicate_items, join_items, origin_to_gem, add_empty, make_child, emptytocenter, hide, white_background, select_activate, camera_view, delete_obj, makeparent, hidden_status, delete_extra_objects

class Video_OT_objectstocenter(bpy.types.Operator):
    """ """
    bl_label = "Objects to center"
    bl_idname = "object.objectstocenter"
    bl_options = {"REGISTER", "UNDO"}
    
    
    def execute(self, context):
        global joined, initial_objects_list_name, empty_name

        initial_objects_list = list(bpy.context.selected_objects)
        initial_objects_list_name = [item.name for item in list(bpy.context.selected_objects)]

        if len(initial_objects_list) >1:
            joined = " &".join(item for item in initial_objects_list_name)
        else:
            joined = initial_objects_list_name[0] + ' joined'

        status = check_obj(joined)
        if status:
            pass

        else:       
            duplicate_list = duplicate_items(initial_objects_list, joined)      
            join_items(duplicate_list, joined)
        
            origin_to_gem(bpy.data.objects[joined])
        
            bpy.ops.view3d.snap_cursor_to_selected()
        
            empty_name = add_empty(bpy.data.objects[joined], joined)
        
            make_child(initial_objects_list, bpy.data.objects[empty_name])
        
            emptytocenter(bpy.data.objects[empty_name])
        
            hide(bpy.data.objects[joined])

        return {'FINISHED'}
    
        
class Video_OT_camera(bpy.types.Operator):
    """ """
    bl_label = "Add camera"
    bl_idname = "object.addcamera"
    bl_options = {"REGISTER", "UNDO"}
        
    
    def execute(self, context):
        white_background()
        
        dimensions = bpy.data.objects[joined].dimensions
        rad = math.sqrt((dimensions[0]/2)**2 + (dimensions[1]/2)**2 + (dimensions[2]/2)**2)
        print(rad)
        
        bpy.ops.curve.primitive_bezier_circle_add(radius=rad, enter_editmode=False, align='WORLD')
        bpy.context.object.name = 'my_path'

        bpy.context.scene.transform_orientation_slots[0].type = 'VIEW'
        bpy.ops.transform.transform(mode='ALIGN')
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='VIEW',orient_matrix_type='VIEW', constraint_axis=(True, False, False))
        
        
        bpy.context.space_data.overlay.show_overlays = False
        bpy.context.space_data.lock_camera = False
        

        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
        bpy.ops.transform.transform(mode='ALIGN')
        bpy.context.object.name = '360_empty'

        status = check_obj('my_cam')
        if status:
            delete_obj(bpy.data.objects['my_cam'])

        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW')
        bpy.context.object.name = 'my_cam'
        bpy.context.object.data.type = 'ORTHO'
        bpy.data.scenes['Scene'].camera = bpy.data.objects['my_cam']

        bpy.ops.transform.translate(value=(0, 0, rad), orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(False, False, True))
        
        
        camera_view()
        
        makeparent(empty_name)
        
        return {'FINISHED'}
    
    
class Video_OT_saveanimation(bpy.types.Operator):
    """ """
    bl_label = "Save animation"
    bl_idname = "object.saveanimation"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        select_activate(bpy.data.objects["360_empty"])
        bpy.context.scene.frame_end = 200
        
        
        if mytool.axis_selection == 'OP1':
            for myframe in range (10, 190):
                bpy.ops.transform.rotate(value=0.034906585, orient_axis='Y', orient_type='LOCAL', orient_matrix_type='LOCAL' , constraint_axis=(False, True, False))
                bpy.data.objects['360_empty'].keyframe_insert(data_path = 'rotation_euler', frame = myframe)
        else:
            for myframe in range (10, 190):
                bpy.ops.transform.rotate(value=0.034906585, orient_axis='Z', orient_type='LOCAL', orient_matrix_type='LOCAL' , constraint_axis=(False, False, True))
                bpy.data.objects['360_empty'].keyframe_insert(data_path = 'rotation_euler', frame = myframe)
            

        hidden_status()
        bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.codec = 'H264'

        scene = context.scene
        mytool = scene.my_tool
        filepath = mytool.myfilepath
        filename = mytool.myfilename
        bpy.context.scene.render.filepath = filepath+filename
        bpy.ops.render.render(animation=True)
        
       
        
        return {'FINISHED'}
        

class Image_OT_Clear(bpy.types.Operator):
    """ """
    bl_label = "Clear"
    bl_idname = "object.clear"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
               
        delete_extra_objects(initial_objects_list_name)     

        return {'FINISHED'}
    
