import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty


class QuickMocapAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = 'quickmocap.base'
    print("NAMEEEE PREFF ", __package__)
    female_model_path: StringProperty(
        name="Female SMPL fbx File Path",
        subtype='FILE_PATH',
        default='C:/temp/mocap/smpl/SMPL_f_unityDoubleBlends_lbs_10_scale5_207_v1.0.0.fbx'
        
    )
    male_model_path: StringProperty(
        name="Male SMPL fbx File Path",
        subtype='FILE_PATH',
        default='C:/temp/mocap/smpl/SMPL_m_unityDoubleBlends_lbs_10_scale5_207_v1.0.0.fbx'
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Set these preferences")
        layout.prop(self, "female_model_path")
        layout.prop(self, "male_model_path")

