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
def find_and_replace(
        source_type,
        replacement_type,
        replacement_path,
        material_path="",
        directory_path="",
        recursive_search=True,
        material_name="",
        custom_name="",
        delete_nodes=True
    ):

    if not material_path and not directory_path:
        print("Please supply a path to the material or a directory path to search under")
        return

    to_search = []

    if material_path:
        mat = load_asset(material_path)
        to_search.append(mat)
    else:
        asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
        materials = [asset for asset in asset_reg.get_assets_by_path(directory_path, recursive=recursive_search) if asset.asset_class_path.asset_name == "Material"]
        if material_name:
            for mat in materials:
                if mat.asset_name == material_name:
                    to_search.append(mat.get_asset())
        else:
            to_search = [mat.get_asset() for mat in materials]

    for material in to_search:
        perform_find_replace(material, source_type, replacement_type, replacement_path, custom_name, delete_nodes)

def perform_find_replace(
        material,
        source_type,
        replacement_type,
        replacement_path,
        custom_name="",
        delete_nodes=True
    ):
    replacement_asset = load_asset(replacement_path)

    expressions = unreal.PythonMaterialLib.get_material_expressions(material)
    to_replace = [expression for expression in expressions if source_type in expression.get_name()]

    if not to_replace:
        # no matches found
        return

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
            new_name = custom_name + " {}".format(index + 1) if len(to_replace) > 1 else custom_name
            new_node.set_editor_property("parameter_name", new_name)
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

# material path example
'''
find_and_replace(
    material_path="/Game/FindReplaceMatExample/M_TestOnMeToo",
    source_type="MaterialExpressionVertexColor",
    replacement_type=unreal.MaterialExpressionTextureSampleParameter2D,
    replacement_path="/Game/FindReplaceMatExample/T_GenericBrickGlass_M",
    custom_name="RGB Mask",
    delete_nodes=False
)
'''

# directory path example
# searches recursively by default
find_and_replace(
    directory_path="/Game/FindReplaceMatExample",
    #material_name="M_TestOnMeToo",
    #recursive_search=False,
    source_type="MaterialExpressionVertexColor",
    replacement_type=unreal.MaterialExpressionTextureSampleParameter2D,
    replacement_path="/Game/FindReplaceMatExample/T_GenericBrickGlass_M",
    custom_name="RGB Mask",
    delete_nodes=False
)