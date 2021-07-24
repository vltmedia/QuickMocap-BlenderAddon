# Checks if a script is running in Blender or not
import os
import sys

def check_if_in_blender():
    in_blender = False
    try:
        import bpy      
        in_blender = not bpy.app.background
    except:
        in_blender = False
    return in_blender