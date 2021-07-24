# Example Usage:
# CleanPoseKeys(clean_threshold = 0.001, use_channels = False,smooth_iterations = 5,all_bones = True, target_bone = "")

import bpy


class CleanPoseKeys:
    def __init__(self, clean_threshold = 0.001, use_channels = False,smooth_iterations = 1,all_bones = True, target_bone = ""):
        self.clean_threshold = clean_threshold
        self.use_channels = use_channels
        self.smooth_iterations = smooth_iterations
        self.all_bones = all_bones
        self.target_bone = target_bone
        self.run_process()
        
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
                self.chosen_bone = bpy.context.object.data.bones.get(self.target_bone)
                self.chosen_bone.select = True
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
            
    def smooth_iterate(self):
        # Run the smooth iterations for smoothing the keys
        for iteration in range(0,self.smooth_iterations - 1):
            bpy.ops.graph.smooth()

if __name__ == '__main__':
    cleanPoseKeys = CleanPoseKeys(clean_threshold = 0.001, use_channels = False,smooth_iterations = 5,all_bones = True, target_bone = "")