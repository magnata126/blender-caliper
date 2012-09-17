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

import bpy, mathutils, time
from bpy.app.handlers import persistent

# ########################################################
# By macouno
# ########################################################



# DRIVER TO UPDATE THE CALIPERS
def CaliperUpdate(textCurve, distance):
	# Just set the textCurve's body as the distance... done
	bpy.data.curves[textCurve].body = str(round(distance,6))

	return distance #dist.length

# LOAD THE CALIPER INTO THE DRIVER NAMESPACE ON FILE LOAD	
@persistent
def load_caliper_on_load_file(dummy):
	bpy.app.driver_namespace['CaliperUpdate'] = CaliperUpdate

# LOAD THE CALIPER INTO THE DRIVER NAMESPACE ON SCENE UPDATE	
@persistent
def load_caliper_on_scene_update(dummy):

	if not bpy.app.driver_namespace.get('CaliperUpdate'):
		bpy.app.driver_namespace['CaliperUpdate'] = CaliperUpdate

	# Hack to update all curves that have a text body... hack!
	try:
		for c in bpy.data.curves:
			try:
				c.body = c.body
			except:
				pass
	except:
		pass

		
# Make a new caliper!
def makeCaliper(context):

	bpy.ops.object.select_all(action='DESELECT')

	scn = context.scene
	
	# Add the caliper empty
	caliper = bpy.data.objects.new('caliper', None)
	scn.objects.link(caliper)
	
	# Make an empty for the start of measurement
	start = bpy.data.objects.new('start', None)
	scn.objects.link(start)
	#start.hide_select = True
	start.parent = caliper
	#start.select = True
	
	end = bpy.data.objects.new('end', None)
	scn.objects.link(end)
	#end.hide_select = True
	end.parent = start
	#end.select = True
	#end.location[0] = 2.0
	
	# Add a custom measurement property to the caliper's end
	end['length'] = 0.0
	
	# Add the driver to the measurement so it gets auto updated
	fcurve = end.driver_add('["length"]')
	drv = fcurve.driver
	drv.type = 'SCRIPTED'
	
	drv.show_debug_info = True
	
	# Make a new variable that measures the distance!
	nvar = drv.variables.new()
	nvar.name = 'distance'
	nvar.type = 'LOC_DIFF'
	
	# Make the caliper the start of the measurement
	targ1 = nvar.targets[0]
	targ1.id = start
	
	# Make the end itself the end of the measurement
	targ2 = nvar.targets[1]
	targ2.id = end
	
	
	
	# Now lets see if we can add a text object
	crv = bpy.data.curves.new("length", 'FONT')
	crv.align = 'CENTER'
	crv.offset_y = 0.25
	text = bpy.data.objects.new(crv.name, crv)
	scn.objects.link(text)
	text.parent = caliper
	
	# Lets add a mesh for the indication
	me = bpy.data.meshes.new('arrow')
	arrow = bpy.data.objects.new('arrow', me)
	scn.objects.link(arrow)
	arrow.parent = caliper
	
	coList = [(0.1,-0.1,-0.1),(0.1,0.1,-0.1),(-0.1,0.1,-0.1),(-0.1,-0.1,-0.1),(0.1,-0.1,0.1),(0.1,0.1,0.1),(-0.1,0.1,0.1),(-0.1,-0.1,0.1),(0.0,0.0,0.0),(-0.0,0.0,0.0),(0.0,0.0,0.0)]
	poList = [(5,6,2,1),(5,1,9),(7,4,0,3),(0,1,2,3),(7,6,5,4),(7,3,8),(8,2,6),(3,2,8),(6,7,8),(4,5,9),(0,4,9),(1,0,9)]
	sList = [0,1,4,5,9]
	eList = [2,3,6,7,8]
	
	me.from_pydata(coList, [], poList)
	
	
	# Add vertex groups for the start and end
	sGroup = arrow.vertex_groups.new('start')
	sGroup.add(sList, 1.0, 'REPLACE')
	sHook = arrow.modifiers.new('startHook', 'HOOK')
	sHook.vertex_group = sGroup.name
	sHook.object = start
	
	
	eGroup = arrow.vertex_groups.new('end')
	eGroup.add(eList, 1.0, 'REPLACE')
	eHook = arrow.modifiers.new('endHook', 'HOOK')
	eHook.vertex_group = eGroup.name
	eHook.object = end
	
	# Select the arrow object
	arrow.select = True
	scn.objects.active = arrow
	bpy.ops.object.mode_set(mode='EDIT')
	
	bpy.ops.object.hook_reset(modifier=sHook.name)
	bpy.ops.object.hook_reset(modifier=eHook.name)
	
	bpy.ops.object.mode_set(mode='OBJECT')
	
	start.location[0] = -2.5
	end.location[0] = 5.0
	
	
	# AT THE VERY END
	# Set the expression to use the variable we created
	drv.expression = 'CaliperUpdate("'+crv.name+'", '+nvar.name+')'

	
	
	
# FUNCTION TO ADD A CALIPER TO THE SCENE
class Add_Caliper(bpy.types.Operator):
	bl_idname = "object.add_caliper"
	bl_label = "Caliper"
	bl_options = {'REGISTER', 'UNDO'}
		

	def execute(self, context):
		print('adding caliper')
		
		makeCaliper(context)
		
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