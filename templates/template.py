import bpy
from bpy.props import IntProperty, PointerProperty, BoolProperty, CollectionProperty,FloatProperty

from bpy.types import Panel, PropertyGroup, WindowManager

# This is the tab area
class swapObjectVars(PropertyGroup):
    NamePattern: bpy.props.StringProperty(name="Source Name Pattern", default="Cube.*")
    TemplateObject: bpy.props.StringProperty(name="Template Object Name", default="Template")





# class SwapNameSettings(bpy.types.PropertyGroup):
#     NamePattern: bpy.props.StringProperty()
#     TemplateObjectName: bpy.props.StringProperty()
#     PostScale: bpy.props.FloatProperty()

# bpy.utils.register_class(SwapNameSettings)
class OBJECT_OT_swapobjectsingle(bpy.types.Operator):
    bl_idname = 'object.swapobjectsingle'
    bl_label = 'Swap Object Single'
    bl_options = {'REGISTER', 'UNDO'}
    NamePattern: bpy.props.StringProperty(name="Source Name Pattern", default="Cube.*")
    TemplateObject: bpy.props.StringProperty(name="Template Object Name", default="Template")


    def execute(self, context):
        bpy.ops.object.select_pattern(pattern= self.NamePattern)
        selects = context.selected_objects
        currentcount = 0
        transformss = []
        for obj in selects:
            transformss.append([obj.location, obj.rotation_quaternion, obj.scale])
            
            ob = bpy.data.objects.get(self.TemplateObject)
            # ob = bpy.data.objects.get("Template")
            ob_dup = ob.copy()
            print(ob_dup.name)
            bpy.data.collections['Collection'].objects.link(ob_dup)
            ob_dup.name = 'NewObjectName_' + str(currentcount)
            # template_object = bpy.data.objects.get('Template')
            # template_object = context.selected_objects[0]
            # if template_object:
            # Create the new object by linking to the template's mesh data
            new_object = ob_dup
            obj.hide_viewport = True
            obj.hide_render = True
            # new_object = bpy.data.objects.new('NewObjectName_' + str(currentcount), template_object.data)
            # Create a new animation for the newly created object
            nextcount = currentcount + 1
            currentcount = nextcount
            print(new_object.location)
            
            new_object.location = obj.location
            print(obj.location)
        
            # Link the new object to the appropriate collection

        return {'FINISHED'}

class OBJECT_MT_swapmenu(bpy.types.Menu):
    bl_idname = 'object.swapmenu'
    bl_label = 'Swap Objects'

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_swapobjectsingle.bl_idname)
classes = [
	OBJECT_OT_swapobjectsingle,
	OBJECT_MT_swapmenu
]


class swapObject_PT_panel(Panel):
    bl_idname = 'swapObject_PT_panel'
    bl_label = 'Quick Mocap'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QuickMocap'

    def draw(self, context):
        operator = self.layout.operator('object.swapobjectsingle', icon='BLENDER', text='Swap Objects By Name')
        operator.NamePattern = context.window_manager.swapObject_vars.NamePattern
        operator.TemplateObject = context.window_manager.swapObject_vars.TemplateObject
        self.layout.prop(context.window_manager.swapObject_vars, 'NamePattern')
        self.layout.prop(context.window_manager.swapObject_vars, 'TemplateObject')


# class swapObject_OT_swapbyname(Operator):
#     bl_idname = 'swapObject.swapbyname'
#     bl_label = 'swapObject: swapbyname'
#     bl_description = 'swapObject - swapbyname'
#     bl_options = {'REGISTER', 'UNDO'}

#     NamePattern: bpy.props.StringProperty(name="Source Name Pattern", default="Cube.*")
#     TemplateObject: bpy.props.StringProperty(name="Template Object Name", default="Template")

#     def execute(self, context):
#         bpy.ops.object.select_pattern(pattern= self.NamePattern)
#         selects = context.selected_objects
#         currentcount = 0
#         transformss = []
#         for obj in selects:
#             transformss.append([obj.location, obj.rotation_quaternion, obj.scale])
            
#             ob = bpy.data.objects.get(self.TemplateObject)
#             # ob = bpy.data.objects.get("Template")
#             ob_dup = ob.copy()
#             print(ob_dup.name)
#             bpy.data.collections['Collection'].objects.link(ob_dup)
#             ob_dup.name = 'NewObjectName_' + str(currentcount)
#             # Create the new object by linking to the template's mesh data
#             new_object = ob_dup
#             obj.hide_viewport = True
#             obj.hide_render = True
#             # new_object = bpy.data.objects.new('NewObjectName_' + str(currentcount), template_object.data)
#             # Create a new animation for the newly created object
#             nextcount = currentcount + 1
#             currentcount = nextcount
#             print(new_object.location)
            
#             new_object.location = obj.location
#             print(obj.location)
        
#         return {'FINISHED'}

#     @classmethod
#     def poll(cls, context):
#         return True


















def register():
    bpy.utils.register_class(swapObjectVars)
    bpy.utils.register_class(swapObject_PT_panel)
    WindowManager.swapObject_vars = PointerProperty(type=swapObjectVars)

    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError as e:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)


