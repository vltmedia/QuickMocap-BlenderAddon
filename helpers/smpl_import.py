# -*- coding: utf-8 -*-
# This Class implimentation is written by Justin Jaro of VLT Media LLC
# Contact: Github VLTMedia
# Copyright©2021 Justin Jaro
# Original non class code license copright below.


# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# You can only use this computer program if you have closed
# a license agreement with MPG or you get the right to use the computer
# program from someone who is authorized to grant you that right.
# Any use of the computer program without a valid license is prohibited and
# liable to prosecution.
#
# Copyright©2019 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# Contact: ps-license@tuebingen.mpg.de
#
# Author: Joachim Tesch, Max Planck Institute for Intelligent Systems, Perceiving Systems
#
# Create keyframed animated skinned SMPL mesh from .pkl pose description
#
# Generated mesh will be exported in FBX or glTF format
#
# Notes:
#  + Male and female gender models only
#  + Script can be run from command line or in Blender Editor (Text Editor>Run Script)
#  + Command line: Install mathutils module in your bpy virtualenv with 'pip install mathutils==2.81.2'




import os
import sys
import bpy
import time
import platform
# import joblib
import argparse
import numpy as np
import addon_utils
from math import radians
from mathutils import Matrix, Vector, Quaternion, Euler


args = []
class SMPL_Importer:

    def __init__(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons['QuickClean-MocapAddon'].preferences
        # Globals
        # Add your UNIX paths here!
        self.male_model_path = addon_prefs.male_model_path
    
        self.female_model_path = addon_prefs.female_model_path
            
        self.fps_source = 30
        self.fps_target = 30

        self.gender = 'female' #female

        self.start_origin = 1
        self.person_id = 0
        

        self.bone_name_from_index = {
            0 : 'Pelvis',
            1 : 'L_Hip',
            2 : 'R_Hip',
            3 : 'Spine1',
            4 : 'L_Knee',
            5 : 'R_Knee',
            6 : 'Spine2',
            7 : 'L_Ankle',
            8: 'R_Ankle',
            9: 'Spine3',
            10: 'L_Foot',
            11: 'R_Foot',
            12: 'Neck',
            13: 'L_Collar',
            14: 'R_Collar',
            15: 'Head',
            16: 'L_Shoulder',
            17: 'R_Shoulder',
            18: 'L_Elbow',
            19: 'R_Elbow',
            20: 'L_Wrist',
            21: 'R_Wrist',
            22: 'L_Hand',
            23: 'R_Hand'
        }


        self.bone_name_from_index_character = {
            0 : 'Hips',
            1 : 'RightUpLeg',
            2 : 'LeftUpLeg',
            3 : 'Spine',
            4 : 'RightLeg',
            5 : 'LeftLeg',
            6 : 'Spine1',
            7 : 'RightFoot',
            8: 'LeftFoot',
            9: 'Spine2',
            10: 'LeftToeBase',
            11: 'RightToeBase',
            12: 'Neck',
            13: 'LeftHandIndex1',
            14: 'RightHandIndex1',
            15: 'Head',
            16: 'LeftShoulder',
            17: 'RightShoulder',
            18: 'LeftArm',
            19: 'RightArm',
            20: 'LeftForeArm',
            21: 'RightForeArm',
            22: 'LeftHand',
            23: 'RightHand'
        }

    # Helper functions

    # Computes rotation matrix through Rodrigues formula as in cv2.Rodrigues
    # Source: smpl/plugins/blender/corrective_bpy_sh.py
    def Rodrigues(self,rotvec):
        theta = np.linalg.norm(rotvec)
        r = (rotvec/theta).reshape(3, 1) if theta > 0. else rotvec
        cost = np.cos(theta)
        mat = np.asarray([[0, -r[2], r[1]],
                        [r[2], 0, -r[0]],
                        [-r[1], r[0], 0]])
        return(cost*np.eye(3) + (1-cost)*r.dot(r.T) + np.sin(theta)*mat)


    # Setup scene
    def setup_scene(self,model_path, fps_target):
        scene = bpy.data.scenes['Scene']

        ###########################
        # Engine independent setup
        ###########################

        scene.render.fps = fps_target

        # Remove default cube
        if 'Cube' in bpy.data.objects:
            bpy.data.objects['Cube'].select_set(True)
            bpy.ops.object.delete()

        # Import gender specific .fbx template file
        bpy.ops.import_scene.fbx(filepath=model_path)


    # Process single pose into keyframed bone orientations
    def process_pose(self,current_frame, pose, trans, pelvis_position):

        if pose.shape[0] == 72:
            rod_rots = pose.reshape(24, 3)
        else:
            rod_rots = pose.reshape(26, 3)

        mat_rots = [self.Rodrigues(rod_rot) for rod_rot in rod_rots]

        # Set the location of the Pelvis bone to the translation parameter
        armature = bpy.data.objects['Armature']
        self.bones = armature.pose.bones

        # Pelvis: X-Right, Y-Up, Z-Forward (Blender -Y)

        # Set absolute pelvis location relative to Pelvis bone head
        try:
            self.bones[self.bone_name_from_index[0]].location = Vector((100*trans[1], 100*trans[2], 100*trans[0])) - pelvis_position
        except :
            # Handle missing / wrong gender bones. This will change the models gender if a problem is found and continue on.
            bonename = self.bone_name_from_index[0]
            if "m_" in bonename:
                for bone in self.bone_name_from_index:
                    self.bone_name_from_index[bone] = self.bone_name_from_index[bone].replace("m_", "f_")
                    
                self.bone_name_from_index[0] = bonename.replace("m_", "f_")
                self.bones[bonename.replace("m_", "f_")].location = Vector((100*trans[1], 100*trans[2], 100*trans[0])) - pelvis_position
                
                
            if "f_" in bonename:
                for bone in self.bone_name_from_index:
                    bone = bone.replace("f_", "m_")
                self.bone_name_from_index[0] = bonename.replace("f_", "m_")
                self.bones[bonename.replace("f_", "m_")].location = Vector((100*trans[1], 100*trans[2], 100*trans[0])) - pelvis_position
                
        # bones['Root'].location = Vector(trans)
        self.bones[self.bone_name_from_index[0]].keyframe_insert('location', frame=current_frame)

        for index, mat_rot in enumerate(mat_rots, 0):
            if index >= 24:
                continue

            bone = self.bones[self.bone_name_from_index[index]]

            bone_rotation = Matrix(mat_rot).to_quaternion()
            quat_x_90_cw = Quaternion((1.0, 0.0, 0.0), radians(-90))
            quat_x_n135_cw = Quaternion((1.0, 0.0, 0.0), radians(-135))
            quat_x_p45_cw = Quaternion((1.0, 0.0, 0.0), radians(45))
            quat_y_90_cw = Quaternion((0.0, 1.0, 0.0), radians(-90))
            quat_z_90_cw = Quaternion((0.0, 0.0, 1.0), radians(-90))

            if index == 0:
                # Rotate pelvis so that avatar stands upright and looks along negative Y avis
                bone.rotation_quaternion = (quat_x_90_cw @ quat_z_90_cw) @ bone_rotation
            else:
                bone.rotation_quaternion = bone_rotation

            bone.keyframe_insert('rotation_quaternion', frame=current_frame)

        return


    # Process all the poses from the pose file
    def process_poses(self,
            input_path,
            gender,
            fps_source,
            fps_target,
            start_origin,
            current_context,      

            person_id=0,
            
            rotate_y=True,
            rotate_neg=False,
    ):
        self.input_path = input_path
        self.gender = gender
        self.fps_source = fps_source
        self.fps_target = fps_target
        self.start_origin = start_origin
        self.person_id = person_id
        self.rotate_y = rotate_y
        self.rotate_neg = rotate_neg
        self.context = current_context
        print('Processing: ' + self.input_path)
        
        data = np.load(self.input_path, allow_pickle=True)['results'][()]
        video_name = os.path.basename(self.input_path)
        frame_num = len(list(data.keys()))
        self.poses, self.trans = np.zeros((frame_num, 72)), np.zeros((frame_num, 3))
        for frame_id in range(frame_num):
            self.poses[frame_id] = data['{}'.format(frame_id)][0]['pose']
            self.trans[frame_id] = data['{}'.format(frame_id)][0]['trans']

        if self.gender == 'female':
            model_path = self.female_model_path
            for k,v in self.bone_name_from_index.items():
                self.bone_name_from_index[k] = 'f_avg_' + v
        elif self.gender == 'male':
            model_path = self.male_model_path
            for k,v in self.bone_name_from_index.items():
                self.bone_name_from_index[k] = 'm_avg_' + v
        elif self.gender == 'character':
            model_path = self.character_model_path
            for k,v in self.bone_name_from_index.items():
                self.bone_name_from_index[k] = 'mixamorig1:' + v
        else:
            print('ERROR: Unsupported gender: ' + gender)
            sys.exit(1)

        # Limit target fps to source fps
        if self.fps_target > self.fps_source:
            self.fps_target = self.fps_source

        print('Gender:',gender)
        print('Number of source poses: ',self.poses.shape[0])
        print('Source frames-per-second: ', self.fps_source)
        print('Target frames-per-second: ', self.fps_target)
        print('--------------------------------------------------')

        self.setup_scene(model_path, fps_target)

        self.scene = bpy.data.scenes['Scene']
        self.sample_rate = int(self.fps_source/self.fps_target)
        self.scene.frame_end = (int)(self.poses.shape[0]/self.sample_rate)

        # Retrieve pelvis world position.
        # Unit is [cm] due to Armature scaling.
        # Need to make copy since reference will change when bone location is modified.
        ob = bpy.data.objects['Armature']
        self.armature = ob.data

        bpy.ops.object.mode_set(mode='EDIT')
        # get specific bone name 'Bone'
        pelvis_bone =  self.armature.edit_bones[self.bone_name_from_index[0]]
        # pelvis_bone = armature.edit_bones['f_avg_Pelvis']
        pelvis_position = Vector(pelvis_bone.head)
        bpy.ops.object.mode_set(mode='OBJECT')

        source_index = 0
        frame = 1

        offset = np.array([0.0, 0.0, 0.0])

        while source_index <  self.poses.shape[0]:
            print('Adding pose: ' + str(source_index))

            if start_origin:
                if source_index == 0:
                    offset = np.array([ self.trans[source_index][0],  self.trans[source_index][1], 0])

            # Go to new frame
            self.scene.frame_set(frame)

            self.process_pose(frame,  self.poses[source_index], ( self.trans[source_index] - offset), pelvis_position)
            source_index +=  self.sample_rate
            frame += 1
        self.rotate_armature(self.rotate_y)
        return frame

    def rotate_armature(self,use):
        if use == True:
            # Switch to Pose Mode
            bpy.ops.object.posemode_toggle()
            
            # Find the Armature & Bones
            ob = bpy.data.objects['Armature']
            armature = ob.data
            bones = armature.bones
            rootbone = bones[0]
            
            # Find the Root bone
            for bone in bones:
                if "avg_root" in bone.name:
                    rootbone = bone
                    
            rootbone.select = True
            outputvalue = 1.5708
            if self.rotate_neg:
                outputvalue = outputvalue * -1
            # if self.check_if_in_blender():
                # outputvalue = outputvalue * -1
            print("Rotate Value", outputvalue)
            # Rotate the Root bone by 90 euler degrees on the Y axis. Set --rotate_Y=False if the rotation is not needed.
                # bpy.ops.transform.rotate(value=outputvalue, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                # bpy.ops.transform.rotate(value=-1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
            # else:
                # bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
            bpy.ops.transform.rotate(value=outputvalue, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
            # Revert back to Object Mode
            bpy.ops.object.posemode_toggle()
            
    def check_if_in_blender(self):
        in_blender = False
        try:
            # import bpy      
            in_blender = not bpy.app.background
        except:
            in_blender = False
        return in_blender

    def export_animated_mesh(self,output_path):
        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Fix Rotation
        self.rotate_armature(self.rotate_y)

        # Select only skinned mesh and rig
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Armature'].select_set(True)
        bpy.data.objects['Armature'].children[0].select_set(True)

        if output_path.endswith('.glb'):
            print('Exporting to glTF binary (.glb)')
            # Currently exporting without shape/pose shapes for smaller file sizes
            bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB', export_selected=True, export_morph=False)
        elif output_path.endswith('.fbx'):
            print('Exporting to FBX binary (.fbx)')
            bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True, add_leaf_bones=False)
        else:
            print('ERROR: Unsupported export format: ' + output_path)
            sys.exit(1)

        return

# def rotate_armature():
#     # Switch to Pose Mode
#     bpy.ops.object.posemode_toggle()
    
#     # Find the Armature & Bones
#     ob = bpy.data.objects['Armature']
#     armature = ob.data
#     bones = armature.bones
#     rootbone = bones[0]
    
#     # Find the Root bone
#     for bone in bones:
#         if "avg_root" in bone.name:
#             rootbone = bone
            
#     rootbone.select = True
    
#     # Rotate the Root bone by 90 euler degrees on the Y axis. Set --rotate_Y=False if the rotation is not needed.
#     bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
#     # Revert back to Object Mode
#     bpy.ops.object.posemode_toggle()
    
def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


if __name__ == '__main__':
    
    startTime = time.perf_counter()
    
    SMPL_Importer_ = SMPL_Importer()
        
    # Process pose file
    poses_processed = SMPL_Importer_.process_poses(
            input_path="C:/temp/mocap/smpl/Fail_1_results.npz",
            gender='female',
            fps_source=30,
            fps_target=30,
            start_origin=0,
            person_id=0,
            rotate_y=True,
        )
    
    uimessages = ['Poses processed: '+ str(poses_processed),'Processing time: '+ str(time.perf_counter() - startTime)]
    ShowMessageBox(message=' || '.join(uimessages),  title = "Successfully Imported SMPL!", icon = 'INFO')
    print('--------------------------------------------------')
    print('Poses processed: ', poses_processed)
    print('Processing time : ', time.perf_counter() - startTime)
    print('--------------------------------------------------')
