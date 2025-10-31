import maya.cmds as cmds
import random

class ForestBuilderLogic:
    def assign_color(self, obj_name, color_rgb, shader_name):
        if not cmds.objExists(shader_name):
            material = cmds.shadingNode('lambert', asShader=True, name=shader_name)
            cmds.setAttr(material + ".color", color_rgb[0], color_rgb[1], color_rgb[2], type="double3")
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name + "SG")
            cmds.connectAttr(material + ".outColor", shading_group + ".surfaceShader", force=True)
        else:
            shading_group = shader_name + "SG"
        cmds.select(obj_name)
        cmds.hyperShade(assign=shading_group)
        cmds.select(clear=True)

    def create_ground(self, ground_type):
        if ground_type == "Flat Plane":
            ground_obj = self.create_flat_plane()
            self.assign_color(ground_obj, (0.2, 0.6, 0.2), "FlatPlane_Mat")
        elif ground_type == "Triangle":
            ground_obj = self.create_triangle_flat()
            self.assign_color(ground_obj, (0.4, 0.3, 0.15), "Triangle_Mat")
        elif ground_type == "Circle":
            ground_obj = self.create_circle()
            self.assign_color(ground_obj, (0.6, 0.5, 0.3), "Circle_Mat")

    def create_flat_plane(self):
        cmds.polyCube(name="FlatPlane", width=10, height=0.1, depth=10, sx=5, sy=1, sz=5)
        return "FlatPlane"

    def create_triangle_flat(self):
        verts = [(0, 0, 5), (5, 0, -5), (-5, 0, -5)]
        triangle = cmds.polyCreateFacet(p=verts, n="Triangle")[0]
        return triangle

    def create_circle(self):
        cmds.polyCylinder(name="Circle", radius=5, height=0.1, sx=20, sy=1, sz=1)
        return "Circle"

    
    def create_tree(self, tree_type):
        if tree_type == "Fin Tree":
            self.create_tree1()
        elif tree_type == "Square Tree":
            self.create_tree2()
        elif tree_type == "Circle Tree":
            self.create_tree3()

    def create_tree1(self):
        trunk = cmds.polyCylinder(name="FinTree_Trunk", radius=0.2, height=2)[0]
        leaves = cmds.polyCone(name="FinTree_Leaves", radius=1, height=3)[0]
        cmds.move(0, 2.5, 0, leaves)
        cmds.group(trunk, leaves, name="FinTree_Group")
        self.assign_color(trunk, (0.55, 0.35, 0.2), "Trunk_Mat")
        self.assign_color(leaves, (0.1, 0.5, 0.2), "Pine_Leaves_Mat")

    def create_tree2(self):
        trunk = cmds.polyCube(name="SquareTree_Trunk", width=0.5, height=1.5, depth=0.5)[0]
        leaves = cmds.polyCube(name="SquareTree_Leaves", width=2, height=2, depth=2)[0]
        cmds.move(0, 1.75, 0, leaves)
        cmds.group(trunk, leaves, name="SquareTree_Group")
        self.assign_color(trunk, (0.45, 0.25, 0.1), "Trunk_Mat")
        self.assign_color(leaves, (0.2, 0.65, 0.3), "Block_Leaves_Mat")

    def create_tree3(self):
        trunk = cmds.polyCylinder(name="CircleTree_Trunk", radius=0.1, height=1)[0]
        leaves = cmds.polySphere(name="CircleTree_Leaves", radius=1.5)[0]
        cmds.move(0, 2, 0, leaves)
        cmds.group(trunk, leaves, name="CircleTree_Group")
        self.assign_color(trunk, (0.6, 0.4, 0.2), "Trunk_Mat")
        self.assign_color(leaves, (0.35, 0.7, 0.15), "Bush_Leaves_Mat")

    
    def add_more_trees(self, tree_type, count):
        if tree_type == "None":
            import maya.cmds as cmds
            cmds.warning("กรุณาเลือกชนิดต้นไม้ก่อน")
            return

        for i in range(count):
            if tree_type == "Fin Tree":
                tree = cmds.duplicate("FinTree_Group")[0]
            elif tree_type == "Square Tree":
                tree = cmds.duplicate("SquareTree_Group")[0]
            elif tree_type == "Circle Tree":
                tree = cmds.duplicate("CircleTree_Group")[0]
            else:
                continue

            x = random.uniform(-5, 5)
            z = random.uniform(-5, 5)
            y = 0
            cmds.move(x, y, z, tree)

    
    def cleanup_existing_elements(self):
        try:
            for g in ["FlatPlane", "Triangle", "Circle"]:
                if cmds.objExists(g):
                    cmds.delete(g)

            all_trees = cmds.ls("*Tree*_Group*")
            if all_trees:
                cmds.delete(all_trees)

            for shader_name in ["FlatPlane_Mat", "Triangle_Mat", "Circle_Mat",
                                "Trunk_Mat", "Pine_Leaves_Mat", "Block_Leaves_Mat", "Bush_Leaves_Mat"]:
                if cmds.objExists(shader_name):
                    cmds.delete(shader_name)
                if cmds.objExists(shader_name + "SG"):
                    cmds.delete(shader_name + "SG")
        except Exception:
            pass
