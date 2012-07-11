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
	"version": (0, 1),
	"blender": (2, 6, 3),
	"location": "View3D > Add > Caliper",
	"description": "Add a caliper object",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Object"}

import bpy

# ########################################################
# By macouno
# ########################################################

class Add_Caliper(bpy.types.Operator):
	bl_idname = "object.add_caliper"
	bl_label = "Caliper"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		print('adding caliper')
		bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0,0,0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
		caliper = context.active_object
		caliper.name = 'Caliper'
		return {'FINISHED'}


# Define "Extras" menu
def menu_func(self, context):
 self.layout.operator(Add_Caliper.bl_idname, icon='PLUGIN')


def register():
	bpy.utils.register_module(__name__)

	# Add "Extras" menu to the "Add Mesh" menu
	bpy.types.INFO_MT_add.append(menu_func)


def unregister():
	bpy.utils.unregister_module(__name__)

	# Remove "Extras" menu from the "Add Mesh" menu.
	bpy.types.INFO_MT_add.remove(menu_func)


if __name__ == "__main__":
	register()