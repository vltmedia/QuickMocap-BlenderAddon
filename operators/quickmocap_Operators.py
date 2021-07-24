import bpy
from operators.quickmocap_Op_ImportNumpyMocap import ImportNumpyMocap,ImportNumpyMocap_Clean
from operators.quickmocap_Op_CleanArmature import CleanArmature


class QuickMocap_Operators:

    def __init__(self):
        
        self.classes = [
        ImportNumpyMocap,
        ImportNumpyMocap_Clean,
        CleanArmature
        ]


    def register(self):
        
        for cls in self.classes:
                try:
                    bpy.utils.register_class(cls)
                except ValueError as e:
                    bpy.utils.unregister_class(cls)
                    bpy.utils.register_class(cls)

