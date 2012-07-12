# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
	"name": "Caliper",
	"author": "macouno",
	"version": (2, 1),
	"blender": (2, 6, 3),
	"location": "View3D > Add > Caliper",
	"description": "Add a caliper object",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"}

import bpy
from bpy.app.handlers import persistent

# ########################################################
# By macouno
# ########################################################



# DRIVER TO UPDATE THE CALIPERS
def CaliperUpdate(a):
	return a*0.5

# LOAD THE CALIPER INTO THE DRIVER NAMESPACE ON FILE LOAD	
@persistent
def load_caliper_on_load_file(dummy):
	bpy.app.driver_namespace['CaliperUpdate'] = CaliperUpdate

# LOAD THE CALIPER INTO THE DRIVER NAMESPACE ON SCENE UPDATE	
@persistent
def load_caliper_on_scene_update(dummy):
	if not bpy.app.driver_namespace.get('CaliperUpdate'):
		bpy.app.driver_namespace['CaliperUpdate'] = CaliperUpdate
	
	
	
# FUNCTION TO ADD A CALIPER TO THE SCENE
class Add_Caliper(bpy.types.Operator):
	bl_idname = "object.add_caliper"
	bl_label = "Caliper"
	bl_options = {'REGISTER', 'UNDO'}
		

	def execute(self, context):
		print('adding caliper')
		
		# Add an empty
		bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0,0,0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
		
		# Retrieve a link to the new empty
		caliper = context.active_object
		caliper.name = 'Caliper'
		
		# Add a measurement property to the caliper
		caliper['measurement'] = 0.0
		
		# Add the driver to the measurement so it gets auto updated
		fcurve = caliper.driver_add('["measurement"]')
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = 'CaliperUpdate(frame)'
		drv.show_debug_info = True
		
		return {'FINISHED'}


# Define menu item
def menu_func(self, context):
	self.layout.operator(Add_Caliper.bl_idname, icon='PLUGIN')

# Load and register
def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_add.append(menu_func)
	
	bpy.app.handlers.load_post.append(load_caliper_on_load_file)
	bpy.app.handlers.scene_update_pre.append(load_caliper_on_scene_update)

# Unregister
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_add.remove(menu_func)


if __name__ == "__main__":
	register()