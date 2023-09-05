import unreal

from pprint import pprint
import tutorial_scripts as ts


def get_material_expressions(mat_instance):

    expressions = unreal.PythonMaterialLib.get_material_expressions(mat_instance)

    exp_dict = {}
    for exp in expressions:
        name = exp.get_name()
        if name not in exp_dict:
            exp_dict[name] = []
        
        exp_dict[name].append(exp)

    return exp_dict.keys()


def get_MaterialExpressionLinearInterpolate(mat_instance):
    expressions = unreal.PythonMaterialLib.get_material_expressions(mat_instance)

    for exp in expressions:
        name = exp.get_name()
        if "MaterialExpressionLinearInterpolate" in name.split("_"):
            return exp
    
    return None

constants_mat = ts.load_asset('/Game/FindReplaceMatExample/M_TestOnMe.M_TestOnMe')
vertex_mat = ts.load_asset('/Game/FindReplaceMatExample/M_TestOnMeToo.M_TestOnMeToo')

c_mat_exp = get_material_expressions(constants_mat)
ver_mat_exp = get_material_expressions(vertex_mat)

lerp = get_MaterialExpressionLinearInterpolate(constants_mat)


unreal.PythonMaterialLib.log_mat(constants_mat)


# from importlib import reload

# ts.list_asset_paths()

# disco_ball = ts.load_asset('/Game/FindReplaceMatExample/ExampleMats/M_FRMExampleAfter.M_FRMExampleAfter')
# print(disco_ball)
# print(disco_ball.get_editor_property("physical_material_map"))
# test_on_me_too_load = ts.load_asset('/Game/FindReplaceMatExample/M_TestOnMeToo.M_TestOnMeToo')
# print(test_on_me_too_load.get_editor_property("enable_mobile_separate_translucency"))
# test_on_me_too_load.set_editor_property("enable_mobile_separate_translucency", True)
# print(test_on_me_too_load.get_editor_property("enable_mobile_separate_translucency"))




# material expresion. vertex color. 

# # test_on_me_too_load.allow_negative_emissive_color(True)
# print(test_on_me_too_load.get_editor_property("EmissiveColor"))
# test_on_me_too_load.set_editor_property("Emissive Color", unreal.LinearColor(r=0.0, g=1.0, b=0.0, a=0.0))
# test_on_me_too_load.enable_mobile_separate_translucency(True)
# test_on_me_too = unreal.EditorAssetLibrary.find_asset_data('/Game/FindReplaceMatExample/M_TestOnMeToo.M_TestOnMeToo').get_asset()
# print(test_on_me_too)

# m_selected_nodes = [node.__class__ for node in unreal.MaterialEditingLibrary.get_material_selected_nodes(test_on_me_too)]
# print(f"Selected Node: {m_selected_nodes}")

# m_property = unreal.MaterialEditingLibrary.get_material_property_input_node(test_on_me_too, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
# print(m_property)
# unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(test_on_me_too, "Emissive Color", unreal.LinearColor(r=0.0, g=1.0, b=0.0, a=0.0))

# glow = ts.load_asset('/Game/FindReplaceMatExample/ExampleMats/M_FRMExampleBefore.M_FRMExampleBefore')
# print(unreal.MaterialEditingLibrary.get_material_default_vector_parameter_value(glow, 'Color'))

# unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(glow, "Diffuse Main Map Brightness", 42)
# unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(glow, 'Color', unreal.LinearColor(r=0.5, g=0.0, b=0.0, a=1.0))
# unreal.MaterialEditingLibrary.update_material_instance(glow)
# print(unreal.MaterialEditingLibrary.get_material_default_vector_parameter_value(glow, 'Color'))




