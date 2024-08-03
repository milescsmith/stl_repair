from pathlib import Path

import bpy
from loguru import logger

bpy.ops.preferences.addon_enable(module="object_print3d_utils")


def repair_stl(filename: Path, output_dir: Path | None = None, suffix: str | None = None) -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.wm.stl_import(filepath=str(filename.resolve()), directory=str(filename.resolve().parent))
    bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_VOLUME", center="MEDIAN")

    for i in range(3):
        bpy.context.object.location[i] = 0

    bpy.ops.mesh.print3d_check_all()
    bpy.ops.mesh.print3d_clean_non_manifold()
    bpy.ops.object.collection_instance_add("INVOKE_DEFAULT")
    if suffix:
        bpy.data.objects[0].name = bpy.data.objects[0].name + suffix
    if not output_dir:
        output_dir = f"{filename.resolve().parent!s}/"
    output_dir = output_dir if isinstance(output_dir, str) else str(output_dir)
    output_dir = output_dir if output_dir.endswith("/") else f"{output_dir}/"

    logger.info(f"{output_dir=}")
    logger.info(f"{bpy.data.objects[0].name=}")
    bpy.ops.wm.stl_export(filepath=output_dir, display_type="DEFAULT", use_batch=True, export_selected_objects=True)
    logger.info(f"Wrote file to {output_dir + bpy.data.objects[0].name + '.stl'}")
    bpy.ops.wm.read_homefile(use_empty=True)
