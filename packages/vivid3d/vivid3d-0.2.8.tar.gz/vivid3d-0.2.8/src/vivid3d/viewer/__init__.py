from . import viewer
from . import volumetric_viewer


def show(model):
    # Works with trimesh and vivid models
    glb = model.export(file_type="glb")
    embedded = viewer.view_glb(glb)
    return embedded
