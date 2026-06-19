"""Logger-all variant: logging module with level=DEBUG, all 30 messages emitted via lazy % formatting."""

import logging
import sys
import pymxs
import random

rt = pymxs.runtime

logger = logging.getLogger("ExplodeGeometry.perf.logger_all")
if not logger.handlers:
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda r: r.levelno < logging.WARNING)
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stderr_handler)

    logger.propagate = False


def _random_wire_color():
    return rt.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def convert_to_triangle_faces(node, addShell=False, shell_amount=1.0,
                               addEditMesh=False, collapseNode=False, centerPivot=False):
    logger.debug("[ExplodeGeometry] [TriMesh] Converting '%s' to mesh...", node.name)
    rt.convertToMesh(node)
    num_faces = rt.getNumFaces(node)
    logger.debug("[ExplodeGeometry] [TriMesh] '%s' has %d face(s) to explode", node.name, num_faces)
    for face_idx in range(1, num_faces + 1):
        face = rt.getFace(node, face_idx)
        v1 = rt.getVert(node, int(face.x))
        v2 = rt.getVert(node, int(face.y))
        v3 = rt.getVert(node, int(face.z))
        logger.debug("[ExplodeGeometry] [TriMesh] Face %d/%d: verts=(%.2f,%.2f,%.2f) (%.2f,%.2f,%.2f) (%.2f,%.2f,%.2f)",
                     face_idx, num_faces, v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, v3.x, v3.y, v3.z)

        new_node = rt.mesh(vertices=rt.Array(v1, v2, v3),
                           faces=rt.Array(rt.Point3(1, 2, 3)))
        rt.update(new_node)
        new_node.wireColor = _random_wire_color()
        logger.debug("[ExplodeGeometry] [TriMesh] Created piece '%s' for face %d", new_node.name, face_idx)

        applySettings(new_node, addShell, shell_amount,
                      addEditMesh, collapseNode, centerPivot)
    logger.debug("[ExplodeGeometry] [TriMesh] Finished exploding '%s'", node.name)


def convert_to_mnmesh_faces(node, addShell=False, shell_amount=1.0,
                             addEditMesh=False, collapseNode=False, centerPivot=False):
    logger.debug("[ExplodeGeometry] [Poly] Converting '%s' to poly...", node.name)
    rt.convertToPoly(node)
    num_faces = rt.polyop.getNumFaces(node)
    logger.debug("[ExplodeGeometry] [Poly] '%s' has %d face(s) to explode", node.name, num_faces)

    for face_idx in range(num_faces, 0, -1):
        logger.debug("[ExplodeGeometry] [Poly] Detaching face %d/%d", face_idx, num_faces)
        rt.polyop.detachFaces(node, rt.Array(face_idx), asNode=True)
        new_node = rt.objects[-1]
        if new_node is None:
            logger.warning("[ExplodeGeometry] [Poly] WARNING: Could not find detached node for face %d", face_idx)
            continue
        new_node.wireColor = _random_wire_color()
        logger.debug("[ExplodeGeometry] [Poly] Created piece '%s' for face %d", new_node.name, face_idx)
        applySettings(new_node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot)
    logger.debug("[ExplodeGeometry] [Poly] Finished exploding '%s'", node.name)


def applySettings(n, addShell, shell_amount, addEditMesh, collapseNode, centerPivot):
    logger.debug("[ExplodeGeometry] applySettings on '%s': shell=%s (amt=%s) editMesh=%s collapse=%s centerPivot=%s",
                 n.name, addShell, shell_amount, addEditMesh, collapseNode, centerPivot)
    if addShell:
        logger.debug("[ExplodeGeometry] Adding Shell modifier (outerAmount=%s)", shell_amount)
        mod = rt.Shell()
        mod.outerAmount = shell_amount
        rt.addModifier(n, mod)

    if addEditMesh:
        logger.debug("[ExplodeGeometry] Adding Edit Mesh modifier")
        mod = rt.Edit_Mesh()
        rt.addModifier(n, mod)

    if collapseNode:
        logger.debug("[ExplodeGeometry] Collapsing modifier stack")
        rt.maxOps.collapseNode(n, True)

    if centerPivot:
        logger.debug("[ExplodeGeometry] Centering pivot")
        rt.centerPivot(n)
