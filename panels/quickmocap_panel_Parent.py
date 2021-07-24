
import bpy
from panels.quickmocap_panel import QuickMocapTemplatePanel 
from bpy.types import Panel, PropertyGroup, WindowManager

class QMOCAP_PT_Parent(QuickMocapTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_Parent_panel'
    bl_label = "Mocap"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "QuickTools"
    bl_context = "objectmode"   
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        quickmocap_tool = scene.quickmocap_tool
        
        layout.separator()
        
        

# class QMOCAP_PT_Parent(Panel):
#     bl_label = "Quick USD"
#     bl_idname = "OBJECT_PT_quickusd_panel"
#     bl_space_type = "VIEW_3D"   
#     bl_region_type = "UI"
#     bl_category = "Quick USD"
#     bl_context = "objectmode"   


#     @classmethod
#     def poll(self,context):
#         return context.object is not None

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
        
#         quickusd_tool = scene.quickusd_tool
#         layout.prop(quickusd_tool, "enum_exportSelection", text="")

#         # layout.prop(quickusd_tool, "outputdir")
#         # layout.prop(quickusd_tool, "enum_objectFlatten", text="") 
#         # layout.prop(quickusd_tool, "enum_exportSelection", text="")
#         # layout.prop(quickusd_tool, "bool_openPostExport")
#         # layout.operator("wm.quickusd_cleanupgeo")
#         # layout.separator()