import bpy

bl_info = {
    "name": "Nestify",
    "author": "KnoxZen",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "3D view > Object > Nestify",
    "description": "Moves selected objects to a new collection with the same name as the parent object and organizes them hierarchically.",
    "category": "Object"
}

def nestify_objects(context):
    # Get selected objects
    selected_objects = context.selected_objects
    
    if len(selected_objects) == 0:
        return {"CANCELLED"}
    
    # Get active object (parent object)
    parent_object = context.active_object
    
    if not parent_object.empty_display_type == 'PLAIN_AXES':
        return {"CANCELLED"}
    
    # Create new collection and set its name
    new_collection = bpy.data.collections.new(parent_object.name)
    
    # Link newly created collection to scene collection
    context.collection.children.link(new_collection)
    
    # Move parent object to the new collection
    parent_object_old_collections = list(parent_object.users_collection)
    for col in parent_object_old_collections:
        col.objects.unlink(parent_object)
    new_collection.objects.link(parent_object)
    
    # Move all children objects to the new collection recursively
    move_children_to_collection(parent_object, new_collection)

def move_children_to_collection(parent_obj, new_collection):
    children_objects = parent_obj.children
    for child_obj in children_objects:
        obj_old_collections = list(child_obj.users_collection)
        for col in obj_old_collections:
            col.objects.unlink(child_obj)
        new_collection.objects.link(child_obj)
        move_children_to_collection(child_obj, new_collection)

class OBJECT_OT_nestify(bpy.types.Operator):
    bl_idname = 'object.nestify'
    bl_label = 'Nestify'
    bl_category = 'Object'

    def execute(self, context):
        nestify_objects(context)
        return {'FINISHED'}

def menu_func(self, context):
    layout = self.layout
    layout.operator(OBJECT_OT_nestify.bl_idname)

classes = (OBJECT_OT_nestify,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
