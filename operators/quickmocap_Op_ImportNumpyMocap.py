import bpy

from helpers.smpl_import import SMPL_Importer 
from helpers.cleanposekeys import CleanPoseKeys 

class ImportNumpyMocap(bpy.types.Operator):
    bl_idname = "wm.quickmocap_importnumpymocap"
    bl_label = "Import Numpy Mocap"
    
    # @classmethod 
    # def poll(cls, context):
    #     ob = context.active_object
    #     return ob and ob.type == 'MESH'
    
    def execute(self, context):
        scene = context.scene
        quickmocap_tool = scene.quickmocap_tool
        SMPL_Importer_ = SMPL_Importer(context)
       
        # # Process pose file
        poses_processed = SMPL_Importer_.process_poses(
                input_path=quickmocap_tool.input_path.replace("\\", "/").replace('"', ""),
                gender=quickmocap_tool.enum_gender,
                fps_source=quickmocap_tool.fps_source,
                fps_target=quickmocap_tool.fps_target,
                start_origin=quickmocap_tool.start_origin,
                person_id=quickmocap_tool.person_id,
                current_context=context,
                
                rotate_y=quickmocap_tool.rotate_y,
                rotate_neg=quickmocap_tool.rotate_neg,
            )

        # Report "Hello World" to the Info Area
        # print("ExportUSD")
        return {'FINISHED'}


class ImportNumpyMocap_Clean(bpy.types.Operator):
    bl_idname = "wm.quickmocap_importnumpymocapclean"
    bl_label = "Import Numpy Mocap & Clean"
    
    # @classmethod 
    # def poll(cls, context):
    #     ob = context.active_object
    #     return ob and ob.type == 'MESH'
    
    def execute(self, context):
        scene = context.scene
        quickmocap_tool = scene.quickmocap_tool
        SMPL_Importer_ = SMPL_Importer(context)
    
        # # Process pose file
        poses_processed = SMPL_Importer_.process_poses(
                input_path=quickmocap_tool.input_path.replace("\\", "/").replace('"', ""),
                gender=quickmocap_tool.enum_gender,
                fps_source=quickmocap_tool.fps_source,
                fps_target=quickmocap_tool.fps_target,
                start_origin=quickmocap_tool.start_origin,
                person_id=quickmocap_tool.person_id,
                current_context=context,
                
                rotate_y=quickmocap_tool.rotate_y,
                rotate_neg=quickmocap_tool.rotate_neg,
            )

        cleanposekeys = CleanPoseKeys(clean_threshold = quickmocap_tool.clean_threshold, use_channels = quickmocap_tool.use_channels,smooth_iterations = quickmocap_tool.smooth_iterations,all_bones = quickmocap_tool.all_bones, target_bone = quickmocap_tool.target_bone, context = context)
        
        # Report "Hello World" to the Info Area
        # print("ExportUSD")
        return {'FINISHED'}

