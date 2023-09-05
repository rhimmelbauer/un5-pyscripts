import unreal

root_dir = '/Game'

def load_asset(asset_path):
    return unreal.EditorAssetLibrary.load_asset(asset_path)


def get_connection_info(connection, expression, node_list):
    node_index = node_list.index(expression)
    output_name = connection.get_editor_property("left_output_name")
    if output_name == "None":
        # check predefined list of outputs based on the index
        output_index = connection.get_editor_property("left_output_index")
        output_name = ["RGB", "R", "G", "B", "A"][output_index]
    return node_index, output_name


# reusable function, to be expanded and generalized further
# relies on TAPython plugin
# currently takes a direct path to the material, but in the future should also be able to search within the project or a given directory
def find_and_replace(material_path, source_type, replacement_type, replacement_path, custom_name="", delete_nodes=True):
    material = load_asset(material_path)
    replacement_asset = load_asset(replacement_path)

    expressions = unreal.PythonMaterialLib.get_material_expressions(material)
    to_replace = [expression for expression in expressions if source_type in expression.get_name()]

    # create new nodes to replace the old ones
    new_nodes = []
    for index, item in enumerate(to_replace):
        x_pos = item.get_editor_property("material_expression_editor_x")
        y_pos = item.get_editor_property("material_expression_editor_y")

        new_node = unreal.MaterialEditingLibrary.create_material_expression(material, replacement_type, x_pos, y_pos)
        # how do we know what additional info needs to be set on other types of nodes?
        if replacement_type == unreal.MaterialExpressionTextureSampleParameter2D:
            # set texture
            new_node.set_editor_property("texture", replacement_asset)

        if custom_name:
            new_node.set_editor_property("parameter_name", custom_name + " {}".format(index + 1))
        new_nodes.append(new_node)

    # replace connections
    for connection in unreal.PythonMaterialLib.get_material_connections(material):
        left_expression = expressions[connection.get_editor_property("left_expression_index")]

        if connection.get_editor_property("right_expression_index") == -1:
            right_expression = material
        else:
            right_expression = expressions[connection.get_editor_property("right_expression_index")]

        if left_expression in to_replace:
            node_index, output_name = get_connection_info(connection, left_expression, to_replace)
            unreal.MaterialEditingLibrary.connect_material_expressions(
                new_nodes[node_index],
                output_name,
                right_expression,
                connection.get_editor_property("right_expression_input_name")
            )
        elif right_expression in to_replace:
            node_index, output_name = get_connection_info(connection, right_expression, to_replace)
            unreal.MaterialEditingLibrary.connect_material_expressions(
                left_expression,
                output_name,
                new_nodes[node_index],
                connection.get_editor_property("right_expression_input_name")
            )

    if delete_nodes:
        for node in to_replace:
            unreal.MaterialEditingLibrary.delete_material_expression(material, node)

find_and_replace(
    material_path="/Game/FindReplaceMatExample/M_TestOnMeToo.M_TestOnMeToo",
    source_type="MaterialExpressionVertexColor",
    replacement_type=unreal.MaterialExpressionTextureSampleParameter2D,
    replacement_path="/Game/FindReplaceMatExample/T_GenericBrickGlass_M.T_GenericBrickGlass_M",
    custom_name="RGB Mask",
    delete_nodes=False
)