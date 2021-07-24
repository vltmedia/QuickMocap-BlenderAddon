import bpy
from bpy.props import IntProperty, PointerProperty, BoolProperty, CollectionProperty,FloatProperty

from bpy.types import Panel, PropertyGroup, WindowManager
from quickmocap_props import QuickMocapProperties



class OBJECT_PT_QuickMocapPanel(Panel):
    bl_label = "Quick Mocap"
    bl_idname = "OBJECT_PT_quickmocap_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Quick Mocap"
    bl_context = "objectmode"   



    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        quickmocap_tool = scene.quickmocap_tool

        # layout.prop(quickmocap_tool, "outputdir")
        # layout.prop(quickmocap_tool, "enum_objectFlatten", text="") 
        # layout.prop(quickmocap_tool, "enum_exportSelection", text="")
        # layout.prop(quickmocap_tool, "bool_openPostExport")
        # layout.operator("wm.quickmocap_cleanupgeo")
        # layout.separator()