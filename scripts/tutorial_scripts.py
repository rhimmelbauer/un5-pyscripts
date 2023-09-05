import unreal

print("hello Unreal Project")

root_dir = '/Game'

############# Editor Asset Library
def get_asset(asset_path):
    eal = unreal.EditorAssetLibrary

    asset_data = eal.find_asset_data(asset_path)

    return asset_data


def load_asset(asset_path):
    return unreal.EditorAssetLibrary.load_asset(asset_path)



def set_asset_color(asset_path):
    mi = unreal.EditorAssetLibrary.load_asset(asset_path)
    unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, 'Color', unreal.LinearColor(r=0.5, g=0.0, b=0.0, a=1.0))
    unreal.MaterialEditingLibrary.update_material_instance(mi)
    unreal.EditorAssetLibrary.save_loaded_asset(mi)



def list_asset_paths():
    eal = unreal.EditorAssetLibrary

    asset_paths = eal.list_assets(root_dir)

    for asset_path in asset_paths:
        print(asset_path)


def get_assets_by_class_name(directory=None, class_name=None):
    eal = unreal.EditorAssetLibrary

    if not directory:
        directory = '/Game'

    asset_paths = eal.list_assets(directory)
    assets = []

    for asset_path in asset_paths:
        asset_data = eal.find_asset_data(asset_path)
        asset_class = asset_data.get_class().get_name()

        if class_name is None:
            assets.append(asset_data)

        if asset_class == class_name:
            assets.append(asset_data)
    
    return assets

def get_static_mesh_import_data():

    static_meshes = get_asset_class_by_type('StaticMesh')

    for static_mesh in static_meshes:
        asset_import_data = static_mesh.get_editor_property('asset_import_data')
        fbx_file_path = asset_import_data.extract_filename()
        print(fbx_file_path)

def set_static_mesh_lod_group(lod_group):

    static_meshes = get_asset_class_by_type('StaticMesh')

    for static_mesh in static_meshes:
        lod_group_info = static_mesh.get_editor_property('load_group')

        if lod_group_info == 'None' and lod_group_info.get_num_lods() == 1:
            static_mesh.set_editor_property('lod_group', lod_group)

def get_static_mesh_lod_data():

    pml = unreal.ProceduralMeshLibraray()
    static_meshes = get_asset_class_by_type('StaticMesh')
    static_mesh_lod_data = []

    for static_mesh in static_meshes:
        lod_count = static_mesh.get_num_lods()
        static_mesh_tri_count = []

        for i in range(lod_count):
            section_count = static_mesh.get_num_sections(i)
            lod_tri_count = 0

            for j in range(section_count):
                section_data = pml.get_section_from_static_mesh(static_mesh, i, j)
                lod_tri_count += len(section_data[1]/3)  # Index one gives out the triangles 

            static_mesh_tri_count.append(lod_tri_count)

        static_mesh_reductions = [100]

        for i in range(1, len(static_mesh_tri_count)):
            static_mesh_reductions.append((static_mesh_tri_count[i] / static_mesh_tri_count[0]) * 100)

        static_mesh_lod_data.append((static_mesh.get_name(), static_mesh_tri_count[1]))
    
    return static_mesh_lod_data

############# Editor Utility Library
def get_selected_assets():
    eul = unreal.EditorUtilityLibrary

    selected_assets = eul.get_selected_assets()

    for selected_asset in selected_assets:
        print(selected_asset)

############# Editor Actor Subsystem
def get_all_actors():

    eas = unreal.EditorActorSubsystem()
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    all_actors = eas.get_all_level_actors()

    for actor in all_actors():
        print(actor)
    
def get_selected_actors():
    eas = unreal.EditorActorSubsystem()

    selected_actors = eas.get_selected_level_actors()

    for selected_actor in selected_actors:
        print(selected_actor)

def get_static_mesh_instance_count():
    level_actors = unreal.EditorActorSubsystem().get_all_level_actors()
    static_mesh_actors = []

    for actor in level_actors:
        if actor.get_class().get_name() == 'StaticMeshActor':
            static_mesh_comp = actor.static_mesh_component
            static_mesh = static_mesh_comp.static_mesh
            static_mesh_actors.append(static_mesh.get_name())

    processed_actors = []

    for static_mesh_actor in static_mesh_actors:
        if static_mesh_actor not in processed_actors:
            processed_actors.append(static_mesh_actor)



