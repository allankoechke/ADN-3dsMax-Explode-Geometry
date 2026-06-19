"""Errors-only variant: 29 debug/info prints removed, only the error print retained."""

import pymxs
import random

rt = pymxs.runtime


def _random_wire_color():
    return rt.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def convert_to_triangle_faces(node, addShell=False, shell_amount=1.0,
                               addEditMesh=False, collapseNode=False, centerPivot=False):
    rt.convertToMesh(node)
    num_faces = rt.getNumFaces(node)
    for face_idx in range(1, num_faces + 1):
        face = rt.getFace(node, face_idx)
        v1 = rt.getVert(node, int(face.x))
        v2 = rt.getVert(node, int(face.y))
        v3 = rt.getVert(node, int(face.z))

        new_node = rt.mesh(vertices=rt.Array(v1, v2, v3),
                           faces=rt.Array(rt.Point3(1, 2, 3)))
        rt.update(new_node)
        new_node.wireColor = _random_wire_color()

        applySettings(new_node, addShell, shell_amount,
                      addEditMesh, collapseNode, centerPivot)


def convert_to_mnmesh_faces(node, addShell=False, shell_amount=1.0,
                             addEditMesh=False, collapseNode=False, centerPivot=False):
    rt.convertToPoly(node)
    num_faces = rt.polyop.getNumFaces(node)

    for face_idx in range(num_faces, 0, -1):
        rt.polyop.detachFaces(node, rt.Array(face_idx), asNode=True)
        new_node = rt.objects[-1]
        if new_node is None:
            print("[ExplodeGeometry] [Poly] WARNING: Could not find detached node for face {}".format(face_idx))
            continue
        new_node.wireColor = _random_wire_color()
        applySettings(new_node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot)


def applySettings(n, addShell, shell_amount, addEditMesh, collapseNode, centerPivot):
    if addShell:
        mod = rt.Shell()
        mod.outerAmount = shell_amount
        rt.addModifier(n, mod)

    if addEditMesh:
        mod = rt.Edit_Mesh()
        rt.addModifier(n, mod)

    if collapseNode:
        rt.maxOps.collapseNode(n, True)

    if centerPivot:
        rt.centerPivot(n)
