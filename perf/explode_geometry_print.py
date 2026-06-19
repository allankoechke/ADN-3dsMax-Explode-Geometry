"""Baseline variant: all 30 print() calls unchanged from the original."""

import pymxs
import random

rt = pymxs.runtime


def _random_wire_color():
    return rt.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def convert_to_triangle_faces(node, addShell=False, shell_amount=1.0,
                               addEditMesh=False, collapseNode=False, centerPivot=False):
    print("[ExplodeGeometry] [TriMesh] Converting '{}' to mesh...".format(node.name))
    rt.convertToMesh(node)
    num_faces = rt.getNumFaces(node)
    print("[ExplodeGeometry] [TriMesh] '{}' has {} face(s) to explode".format(node.name, num_faces))
    for face_idx in range(1, num_faces + 1):
        face = rt.getFace(node, face_idx)
        v1 = rt.getVert(node, int(face.x))
        v2 = rt.getVert(node, int(face.y))
        v3 = rt.getVert(node, int(face.z))
        print("[ExplodeGeometry] [TriMesh] Face {}/{}: verts=({:.2f},{:.2f},{:.2f}) ({:.2f},{:.2f},{:.2f}) ({:.2f},{:.2f},{:.2f})".format(
            face_idx, num_faces, v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, v3.x, v3.y, v3.z))

        new_node = rt.mesh(vertices=rt.Array(v1, v2, v3),
                           faces=rt.Array(rt.Point3(1, 2, 3)))
        rt.update(new_node)
        new_node.wireColor = _random_wire_color()
        print("[ExplodeGeometry] [TriMesh] Created piece '{}' for face {}".format(new_node.name, face_idx))

        applySettings(new_node, addShell, shell_amount,
                      addEditMesh, collapseNode, centerPivot)
    print("[ExplodeGeometry] [TriMesh] Finished exploding '{}'".format(node.name))


def convert_to_mnmesh_faces(node, addShell=False, shell_amount=1.0,
                             addEditMesh=False, collapseNode=False, centerPivot=False):
    print("[ExplodeGeometry] [Poly] Converting '{}' to poly...".format(node.name))
    rt.convertToPoly(node)
    num_faces = rt.polyop.getNumFaces(node)
    print("[ExplodeGeometry] [Poly] '{}' has {} face(s) to explode".format(node.name, num_faces))

    for face_idx in range(num_faces, 0, -1):
        print("[ExplodeGeometry] [Poly] Detaching face {}/{}".format(face_idx, num_faces))
        rt.polyop.detachFaces(node, rt.Array(face_idx), asNode=True)
        new_node = rt.objects[-1]
        if new_node is None:
            print("[ExplodeGeometry] [Poly] WARNING: Could not find detached node for face {}".format(face_idx))
            continue
        new_node.wireColor = _random_wire_color()
        print("[ExplodeGeometry] [Poly] Created piece '{}' for face {}".format(new_node.name, face_idx))
        applySettings(new_node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot)
    print("[ExplodeGeometry] [Poly] Finished exploding '{}'".format(node.name))


def applySettings(n, addShell, shell_amount, addEditMesh, collapseNode, centerPivot):
    print("[ExplodeGeometry] applySettings on '{}': shell={} (amt={}) editMesh={} collapse={} centerPivot={}".format(
        n.name, addShell, shell_amount, addEditMesh, collapseNode, centerPivot))
    if addShell:
        print("[ExplodeGeometry] Adding Shell modifier (outerAmount={})".format(shell_amount))
        mod = rt.Shell()
        mod.outerAmount = shell_amount
        rt.addModifier(n, mod)

    if addEditMesh:
        print("[ExplodeGeometry] Adding Edit Mesh modifier")
        mod = rt.Edit_Mesh()
        rt.addModifier(n, mod)

    if collapseNode:
        print("[ExplodeGeometry] Collapsing modifier stack")
        rt.maxOps.collapseNode(n, True)

    if centerPivot:
        print("[ExplodeGeometry] Centering pivot")
        rt.centerPivot(n)
