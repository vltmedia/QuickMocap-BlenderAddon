
import bpy

from bpy.props import (StringProperty,
                    BoolProperty,
                    IntProperty,
                    FloatProperty,
                    FloatVectorProperty,
                    EnumProperty,
                    PointerProperty,
                    )
from bpy.types import (Panel,
                    Menu,
                    Operator,
                    PropertyGroup,
                    )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class QuickMocapProperties(PropertyGroup):

    # my_float: FloatProperty(
    #     name = "Float Value",
    #     description = "A float property",
    #     default = 23.7,
    #     min = 0.01,
    #     max = 30.0
    #     )

    # my_float_vector: FloatVectorProperty(
    #     name = "Float Vector Value",
    #     description="Something",
    #     default=(0.0, 0.0, 0.0), 
    #     min= 0.0, # float
    #     max = 0.1
    # ) 

    # Clean Props
    smooth_iterations: IntProperty(
        name="Smoothing Iterations",
        description="How many times to smooth the keyframes",
        default=1
        )
    
    clean_threshold: FloatProperty(
        name="Threshold",
        description="Threshold for cleaning the keyframes",
        default=0.001
        )
    
    
    use_channels: BoolProperty(
        name="Use Channels",
        description="Whether to use Channels when Cleaning the Keyframes",
        default=False
        )
    
    in_place: BoolProperty(
        name="In Place",
        description="Whether to process your Target Bone at 0,0,0",
        default=False
        )
    
    all_bones: BoolProperty(
        name="All Bones",
        description="Whether to process a single bone or all the bones in an armature",
        default=False
        )
    
    
    target_bone: StringProperty(
        name="Target Bone",
        description="The name of the bone you want to process",
        default="",
        maxlen=2048,
        )
    
    # Mocap Props
    
        
    input_path: StringProperty(
        name=".npz or .pkl file",
        subtype='FILE_PATH',
        description="The filename of the .npz or .pkl file that holds the poses you want to load.",

        )

    enum_gender: EnumProperty(
        name="Gender",
        description="The Gender you want the mesh to be.",
        items=[ ('female', "Female", ""),
                ('male', "Male", "")
            ]
        )        
    
    fps_source: FloatProperty(
        name = "FPS Source",
        description="The Source Frames Per Second",
        default = 24
        )

    fps_target: FloatProperty(
        name = "FPS Target",
        description="The Target Frames Per Second",
        default = 24
        )

    start_origin: FloatProperty(
        name = "Start Origin",
        default = 0
        )

    person_id: IntProperty(
        name = "Person ID",
        description="The ID of the Person in the file to import.",
        default = 0
        )
    
    rotate_y: BoolProperty(
        name="Rotate Y",
        description="Rotate the object 90 degrees in the Y Axis",
        default=True
        )
    rotate_neg: BoolProperty(
        name="Invert Y Axis Rotation",
        description="Invert the Y Axis Degrees",
        default=False
        )
    
    