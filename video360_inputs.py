import bpy

class video360RenderMyProperties(bpy.types.PropertyGroup):
    myfilepath : bpy.props.StringProperty(name= "Filepath", maxlen = 1000, subtype='DIR_PATH')
    myfilename : bpy.props.StringProperty(name= "Filename", maxlen = 1000, subtype='FILE_NAME')

    axis_selection : bpy.props.EnumProperty(
            name = '',
            description = 'Rotation axis',
            items = [ 
                ('OP1', 'axis parallel to screen', ''),
                ('OP2', 'axis perpendicular to screen' , '')
            ]
        )