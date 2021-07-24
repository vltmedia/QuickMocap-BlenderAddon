
from panels.quickmocap_panel_ImportNMocap import QMOCAP_PT_ImportNMocap
from panels.quickmocap_panel_Cleanup import QMOCAP_PT_Cleanup
import bpy
from bpy.props import IntProperty, PointerProperty, BoolProperty, CollectionProperty,FloatProperty
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty
from bpy.types import Panel, PropertyGroup, WindowManager
from quickUSD import OBJECT_PT_QuickMocapPanel
from quickmocap_props import QuickMocapProperties
from preferences import QuickMocapAddonPreferences

from operators.quickmocap_Operators import QuickMocap_Operators

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Quick Mocap",
    "author" : "Justin Jaro, VLT Media",
    "description" : "Import Numpy mocap & clean it up!",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "3D View > Tools",
    "warning" : "",
    "category" : "Generic"
}

class QuickMocapAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__
    print("NAMEEEE PREFF ", __name__)
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


# bl_idname = 'quickmocap.base'
classes = (
    OBJECT_PT_QuickMocapPanel,
    
    # Populate Child Panels in Order from Top to Bottom

    QMOCAP_PT_ImportNMocap,
    QMOCAP_PT_Cleanup
    
)
operators = QuickMocap_Operators()

def register():

    # WindowManager.swapObject_vars = PointerProperty(type=swapObjectVars)
    try:
        bpy.utils.register_class(QuickMocapProperties)
    except:
        print("QuickClean exists")
    bpy.types.Scene.quickmocap_tool = PointerProperty(type=QuickMocapProperties)
    
    operators.register()
    bpy.utils.register_class(QuickMocapAddonPreferences)
    
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError as e:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)
    
    

def unregister():
    bpy.utils.unregister_class(QuickMocapAddonPreferences)
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.quickmocap_tool

