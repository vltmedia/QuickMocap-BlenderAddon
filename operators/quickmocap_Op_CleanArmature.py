import bpy

from helpers.cleanposekeys import CleanPoseKeys 

class CleanArmature(bpy.types.Operator):
    bl_idname = "wm.quickmocap_cleanarmature"
    bl_label = "Clean Armature Keys"
    

    def execute(self, context):
        scene = context.scene
        quickmocap_tool = scene.quickmocap_tool
        # # Process pose file
        cleanposekeys = CleanPoseKeys(clean_threshold = quickmocap_tool.clean_threshold, use_channels = quickmocap_tool.use_channels,smooth_iterations = quickmocap_tool.smooth_iterations,all_bones = quickmocap_tool.all_bones, target_bone = quickmocap_tool.target_bone, context = context)

        # Report "Hello World" to the Info Area
        # print("ExportUSD")
        return {'FINISHED'}

