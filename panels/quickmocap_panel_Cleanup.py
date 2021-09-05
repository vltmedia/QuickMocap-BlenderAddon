
import bpy
from panels.quickmocap_panel import QuickMocapTemplatePanel 

class QMOCAP_PT_Cleanup(QuickMocapTemplatePanel, bpy.types.Panel):
    bl_idname = 'OBJECT_PT_Cleanup_panel'
    bl_parent_id = "OBJECT_PT_quickmocap_panel"
    bl_label = "Cleanup Armature Keys"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        quickmocap_tool = scene.quickmocap_tool
        layout.label(text="Clean & Smooth your Armature's Keys")

        layout.prop(quickmocap_tool, "all_bones")
        layout.prop(quickmocap_tool, "in_place")
        layout.prop(quickmocap_tool, "use_channels")
        layout.prop(quickmocap_tool, "clean_threshold")
        layout.prop(quickmocap_tool, "smooth_iterations")
        layout.prop(quickmocap_tool, "target_bone")
        # layout.prop(quickmocap_tool, "enum_objectFlatten", text="") 
        layout.operator("wm.quickmocap_cleanarmature")
        # layout.operator("wm.quickmocap_openlastexportedusd")
        
        layout.separator()