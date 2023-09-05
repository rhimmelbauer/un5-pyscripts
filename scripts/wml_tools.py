import unreal


class MaterialExpressionReplace():

    def __init__(self, type) -> None:
        self.get_input_params()

    def get_input_params(self):
        ...


class TextureSampleParameter2DReplacement(MaterialExpressionReplace):

    def get_input_params(self):
        self.input_texture_path()

    def input_texture_path(self):
        self.texture_path = input("Input Texture Path:")
        # TODO: Validate path


SUPPORTED_MATERIAL_EXPRESSION_REPLACEMENTS = {
    unreal.MaterialExpressionTextureSampleParameter2D.__name__: TextureSampleParameter2DReplacement,
}

root_dir = '/Game/'

directory = input("Directory Path to Search & Replace:")

replace = input("Input the Material Expression you would like to replace:")

replace_with = input("Input the Material Expression you would like to replace the original with:")

if replace_with not in SUPPORTED_MATERIAL_EXPRESSION_REPLACEMENTS:
    raise ValueError(f"Material Expression: {replace_with} is not supported")

replacement = SUPPORTED_MATERIAL_EXPRESSION_REPLACEMENTS[replace_with]()

custom_name = input("Input custom name for material expression")

delete_original_expressions = bool(input("Do you wish to delete the original Material Expression (True/False):"))

materials = get_assets_by_class_name(f"{root_dir}{directory}/", "Material")


for material in materials:
    find_and_replace(
        material.get_full_name(),
        replace,
        SUPPORTED_MATERIAL_EXPRESSION_REPLACEMENTS[replace_with],
        replacement.texture_path,
        custom_name,
        delete_original_expressions
    )


