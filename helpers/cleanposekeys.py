# Example Usage:
# CleanPoseKeys(clean_threshold = 0.001, use_channels = False,smooth_iterations = 5,all_bones = True, target_bone = "")

import bpy


class CleanPoseKeys:
    def __init__(self, context,clean_threshold = 0.001, use_channels = False,smooth_iterations = 1,all_bones = True, target_bone = ""):
        self.clean_threshold = clean_threshold
        self.use_channels = use_channels
        self.smooth_iterations = smooth_iterations
        self.all_bones = all_bones
        self.target_bone = target_bone
        self.context = context
        preferences = context.preferences
        self.addon_prefs = preferences.addons['QuickMocap'].preferences
        self.scene = context.scene
        self.quickmocap_tool = self.scene.quickmocap_tool
        self.in_place = self.quickmocap_tool.in_place
        
        self.run_process()
    
    def write_inplace_keys(self):
        scene = bpy.context.scene
        scene.frame_start
        scene.frame_end
        for framee in range( scene.frame_start,scene.frame_end):
            # self.chosen_bone.location = (0, 0, 0)
            bpy.context.object.pose.bones[self.target_bone].location = (0,0,0)
            bpy.context.object.pose.bones[self.target_bone].keyframe_insert("location", frame=framee)
        
        
    def run_process(self):
        self.continue_ = True
        # Go To Pose Mode
        bpy.ops.object.posemode_toggle()

        self.original_type = bpy.context.area.type

        if self.all_bones == True:
        # Select all the bones if all_bones is True
            bpy.ops.pose.select_all(action='SELECT')
        else:
            # Check if the selected object is an Armature, if not don't continue
            if bpy.context.object.type != 'ARMATURE':
                print('Please select an Armature')
                self.continue_ = False
            else:
                # self.chosen_bone = bpy.context.object.pose.bones[self.target_bone]
                self.chosen_bone = bpy.context.object.data.bones.get(self.target_bone)
                self.chosen_bone.select = True
                if self.in_place == True:
                    self.write_inplace_keys()
                print("Selected Bone", self.chosen_bone)

        # If all is good above, continue, else don't
        if self.continue_ == True:
            # Change to graph editor for Context
            bpy.context.area.type = "GRAPH_EDITOR"

            # Select all the keys
            bpy.ops.graph.select_all(action='SELECT')

            # Clean the keys with the settings
            bpy.ops.graph.clean(threshold=self.clean_threshold,channels=self.use_channels)

            # Smooth iteration for smoothing the keys
            self.smooth_iterate()

            # Switch back to original context
            bpy.context.area.type = self.original_type
            bpy.ops.object.posemode_toggle()
            
    def smooth_iterate(self):
        # Run the smooth iterations for smoothing the keys
        for iteration in range(0,self.smooth_iterations - 1):
            bpy.ops.graph.smooth()

if __name__ == '__main__':
    cleanPoseKeys = CleanPoseKeys(clean_threshold = 0.001, use_channels = False,smooth_iterations = 5,all_bones = True, target_bone = "")