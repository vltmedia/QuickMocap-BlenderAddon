
import bpy
from panels.quickmocap_panel import QuickMocapTemplatePanel 

class QMOCAP_PT_ImportNMocap(QuickMocapTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_ImportNPanel_panel'
    bl_parent_id = "OBJECT_PT_quickmocap_panel"
    bl_label = "Import Numpy Mocap"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        quickmocap_tool = scene.quickmocap_tool
        layout.label(text="Import .npz or .pkl")

        layout.prop(quickmocap_tool, "input_path")
        layout.prop(quickmocap_tool, "fps_source")
        layout.prop(quickmocap_tool, "fps_target")
        layout.prop(quickmocap_tool, "start_origin")
        layout.prop(quickmocap_tool, "person_id")
        layout.prop(quickmocap_tool, "rotate_y")
        layout.prop(quickmocap_tool, "rotate_neg")
        layout.prop(quickmocap_tool, "enum_gender")
        # layout.prop(quickmocap_tool, "enum_objectFlatten", text="") 
        layout.operator("wm.quickmocap_importnumpymocap")
        layout.operator("wm.quickmocap_importnumpymocapclean")
        # layout.operator("wm.quickmocap_openlastexportedusd")
        
        layout.separator()