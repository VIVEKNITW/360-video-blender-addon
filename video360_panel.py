import bpy
class Video(bpy.types.Panel):
    """ """
    bl_label = "360 Animation"
    bl_idname = "360video_initialsetup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "360 Video"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        row = layout.row()
        row.operator("object.objectstocenter")
        row = layout.row()
        row.operator("object.addcamera")
        row = layout.row()
        layout.prop(mytool, 'axis_selection')

        row = layout.row()
        row.prop(context.scene.camera.data, 'ortho_scale')
        row = layout.row()
        row.prop(context.scene.camera.data, 'shift_x')
        row = layout.row()
        row.prop(context.scene.camera.data, 'shift_y')
        row = layout.row()
        row.prop(mytool, "myfilename")
        row = layout.row()
        row.prop(mytool, "myfilepath")
        row = layout.row()
        row.operator("object.saveanimation") 