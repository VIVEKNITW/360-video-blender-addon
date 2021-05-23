import bpy
from .video360_helper_functions import deselect, duplicate_items, join_items, origin_to_gem, obj_to_org, make_child, emptytocenter, hidden_status, hide
class Video_objectstocenter(bpy.types.Operator):
    """ """
    bl_label = "Objects to center"
    bl_idname = "object.objectstocenter"
    bl_options = {"REGISTER", "UNDO"}
    
    
    def execute(self, context):
        my_list = bpy.context.selected_objects
        
        deselect()
        
        duplicate_list = duplicate_items(my_list)
          
        deselect()
        
        join_items(duplicate_list)
        
        origin_to_gem(bpy.data.objects["joined"])
        
        bpy.ops.view3d.snap_cursor_to_selected()
        
        obj_to_org(bpy.data.objects["joined"])
        
        make_child(my_list, bpy.data.objects['empty_parent'])
        
        emptytocenter(bpy.data.objects['empty_parent'])
        
        hide(bpy.data.objects['joined'])
        

        
        return {'FINISHED'}
    
        
class Video_camera(bpy.types.Operator):
    """ """
    bl_label = "Add camera"
    bl_idname = "object.addcamera"
    bl_options = {"REGISTER", "UNDO"}
    
    
    
    
    
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'preset_enum')
        
    
    def execute(self, context):
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
        
        
        
        dimensions = bpy.data.objects['joined'].dimensions
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

        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW')
        bpy.context.object.name = 'my_cam'
        bpy.context.object.data.type = 'ORTHO'
        bpy.data.scenes['Scene'].camera = bpy.data.objects['my_cam']

        bpy.ops.transform.translate(value=(0, 0, rad), orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(False, False, True))
        
        
        camera_view()
        
        
        makeparent()
        select_activate(bpy.data.objects["360_empty"])
        bpy.context.scene.frame_end = 200
        
        
        if self.preset_enum == 'OP1':
            for myframe in range (10, 190):
                bpy.ops.transform.rotate(value=0.034906585, orient_axis='Y', orient_type='LOCAL', orient_matrix_type='LOCAL' , constraint_axis=(False, True, False))
                bpy.data.objects['360_empty'].keyframe_insert(data_path = 'rotation_euler', frame = myframe)
        else:
            for myframe in range (10, 190):
                bpy.ops.transform.rotate(value=0.034906585, orient_axis='Z', orient_type='LOCAL', orient_matrix_type='LOCAL' , constraint_axis=(False, False, True))
                bpy.data.objects['360_empty'].keyframe_insert(data_path = 'rotation_euler', frame = myframe)
            
        
        return {'FINISHED'}
    
    
class Video_saveanimation(bpy.types.Operator):
    """ """
    bl_label = "Save animation"
    bl_idname = "object.saveanimation"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
    
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
        
        
        del_objects = ['joined', 'my_path', 'my_cam', "360_empty", 'empty_parent']
        for obj in del_objects:
            unhide(bpy.data.objects[obj])
            select_activate(bpy.data.objects[obj])
            bpy.ops.object.delete()
        
        return {'FINISHED'}
    
