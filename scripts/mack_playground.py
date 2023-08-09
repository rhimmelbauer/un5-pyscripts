import unreal

root_dir = '/Game'

def load_asset(asset_path):
    return unreal.EditorAssetLibrary.load_asset(asset_path)

# specific testcase: find and replace one vertex color that is connected to 3 reroute nodes, using the M_TestOnMe asset
# relies on TAPython plugin

# create new texture expression
test_mat = load_asset('/Game/FindReplaceMatExample/M_TestOnMe.M_TestOnMe')
texture_asset = unreal.load_asset("/Game/FindReplaceMatExample/T_GenericBrickGlass_M.T_GenericBrickGlass_M")

expressions = unreal.PythonMaterialLib.get_material_expressions(test_mat)

vertex_colors = []
reroute_exps = []
for exp in expressions:
    name = exp.get_name()
    if "MaterialExpressionVertexColor" in name:
        vertex_colors.append(exp)
    elif "MaterialExpressionNamedRerouteDeclaration" in name:
        reroute_exps.append(exp)

# eventual goal:
# want to loop through the vertex colors, create a texture sample parameter for each one, and replace at their original position, with pins intact
# for now, just find and replace one

vc_x_pos = vertex_colors[0].get_editor_property("material_expression_editor_x")
vc_y_pos = vertex_colors[0].get_editor_property("material_expression_editor_y")

node_tex = unreal.MaterialEditingLibrary.create_material_expression(test_mat, unreal.MaterialExpressionTextureSampleParameter2D, vc_x_pos, vc_y_pos)
node_tex.set_editor_property("texture", texture_asset)
node_tex.set_editor_property("parameter_name", "RGB Mask")

for reroute in reroute_exps:
    node_color = reroute.get_editor_property("node_color")
    output_name = ""
    if node_color == unreal.LinearColor.RED:
        output_name = "R"
    elif node_color == unreal.LinearColor.BLUE:
        output_name = "B"
    elif node_color == unreal.LinearColor.GREEN:
        output_name = "G"
    unreal.MaterialEditingLibrary.connect_material_expressions(from_expression=node_tex, from_output_name=output_name, to_expression=reroute, to_input_name="")

# delete vertex color(s)
for vc in vertex_colors:
    unreal.MaterialEditingLibrary.delete_material_expression(test_mat, vc)
