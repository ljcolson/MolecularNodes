import os
import bpy
import numpy as np
from . import obj
from . import coll

bpy.types.Scene.mol_import_neuro_path = bpy.props.StringProperty(
    name = 'path_neuro', 
    description = 'File path of the .swc file to open.', 
    options = {'TEXTEDIT_UPDATE'}, 
    default = '', 
    subtype = 'FILE_PATH', 
    maxlen = 0
    )

class MOL_OT_Import_Neuro(bpy.types.Operator):
    bl_idname = "mol.import_neuro"
    bl_label = "Import Neuro SWC"
    bl_description = "Load a SWC file."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        file_neuro = bpy.context.scene.mol_import_neuro_path
        
        object = read(
            path = file_neuro
        )
        bpy.context.view_layer.objects.active = object
        # self.report(
        #     {'INFO'}, 
        #     message=f"Imported "
        #         )
        
        return {"FINISHED"}


def read(path):
    """Access the neuromorpho swc file, strip comments, and load it into the neuroFile nested list. """

    arr = np.loadtxt(path)
    
    edges = arr[:, [0, -1]].astype(int).copy(order = 'c') - 1 # convert to 0 indexing
    edges = np.delete(edges, (0), axis = 0)
    verts = arr[:, [2, 3, 4]].copy(order = 'c')
    radius = arr[:, 5].reshape((1, len(arr)))[0]
    
    neuron = obj.create_object(
        name = "testing", 
        collection = coll.mn(), 
        locations = verts, 
        bonds = edges
    )
    
    obj.add_attribute(
        neuron, 
        'radius', 
        radius
    )

def panel(layout_function, scene):
    col_main = layout_function.column(heading = "", align = False)
    col_main.label(text = "Import Star File")
    row_import = col_main.row()
    # row_import.prop(
    #     bpy.context.scene, 'mol_import_star_file_name', 
    #     text = 'Name', 
    #     emboss = True
    # )
    col_main.prop(
        bpy.context.scene, 'mol_import_neuro_path', 
        text = '.swc file Path', 
        emboss = True
    )
    row_import.operator('mol.import_neuro', text = 'Load', icon = 'FILE_TICK')