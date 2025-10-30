try:
    from PySide6 import QtCore, QtWidgets
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2 import QtCore, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

class ForestBuilderToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Forest Builder')
        self.resize(300, 200)

    
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #B8E0D2,stop:1 #377BA6);
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background-color: #B8E0D2;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QComboBox {
                background-color: white;
                padding: 5px;
            }
        """)

        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        
        GroundLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(GroundLayout)
        self.GroundLabel = QtWidgets.QLabel("Ground Type")
        self.GroundCombo = QtWidgets.QComboBox()
        # เปลี่ยนข้อความใน ComboBox ให้สื่อถึงวัตถุที่สร้าง
        self.GroundCombo.addItems(["None", "Ground1 (Flat Plane)", "Ground2 (Pyramid Hill)", "Ground3 (Cylinder)"])
        GroundLayout.addWidget(self.GroundLabel)
        GroundLayout.addWidget(self.GroundCombo)

        
        treeLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(treeLayout)
        self.treeLabel = QtWidgets.QLabel("Tree Type")
        self.treeCombo = QtWidgets.QComboBox()
        self.treeCombo.addItems(["None", "Tree1", "Tree2", "Tree3"])
        treeLayout.addWidget(self.treeLabel)
        treeLayout.addWidget(self.treeCombo)

        
        buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(buttonLayout)
        self.generateButton = QtWidgets.QPushButton("Create")
        self.generateButton.clicked.connect(self.create_elements)
        buttonLayout.addWidget(self.generateButton)
        self.mainLayout.addStretch()

   
   
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

    def create_elements(self):
        self.cleanup_existing_elements() 
        self.create_ground()
        self.create_tree()

    def create_ground(self):
        ground_type = self.GroundCombo.currentText().split(' ')[0]
        ground_obj = None

        if ground_type == "Ground1":
            ground_obj = self.create_flat_plane() # เปลี่ยนชื่อฟังก์ชัน
            # Ground1 Color: Standard Grass
            self.assign_color(ground_obj, (0.2, 0.6, 0.2), "Ground1_Mat")
        elif ground_type == "Ground2":
            ground_obj = self.create_pyramid_hill() # เปลี่ยนชื่อฟังก์ชัน
            # Ground2 Color: Darker Earth
            self.assign_color(ground_obj, (0.4, 0.3, 0.15), "Ground2_Mat")
        elif ground_type == "Ground3":
            ground_obj = self.create_circle()
            # Ground3 Color: Light Earth
            self.assign_color(ground_obj, (0.6, 0.5, 0.3), "Ground3_Mat")

    def create_flat_plane(self):
        # Ground1: Cube with 5x5 Subdivisions (Flat Plane)
        cmds.polyCube(name="Ground_Plane", width=10, height=0.1, depth=10, sx=5, sy=1, sz=5)
        return "Ground_Plane"

    def create_pyramid_hill(self):
        # Ground2: Creates a Pyramid (Cone with 4 sides) to look like a small hill
        pyramid = cmds.polyCone(name="Ground_Pyramid", radius=5, height=3, sc=1, sa=4, ax=(0, 1, 0))[0]
        # Move it down so the base rests on the origin (Y=0)
        cmds.move(0, -1.5, 0, pyramid, relative=True)
        # Rename the pyramid to "Ground_Plane" for consistency in cleanup
        cmds.rename(pyramid, "Ground_Plane")
        return "Ground_Plane"

    def create_circle(self):
        # Ground3: Cylinder with 20 Sides (Flat Circle)
        cmds.polyCylinder(name="Ground_Plane", radius=5, height=0.1, sx=20, sy=1, sz=1)
        return "Ground_Plane"

    def create_tree(self):
        tree_type = self.treeCombo.currentText()
        
        if tree_type == "Tree1":
            self.create_tree1()
        elif tree_type == "Tree2":
            self.create_tree2()
        elif tree_type == "Tree3":
            self.create_tree3()

    def create_tree1(self):
        """Tree1 (Pine): Cone (Leaves) on a Cylinder (Trunk)."""
        trunk = cmds.polyCylinder(name="Tree1_Trunk", radius=0.2, height=2, sy=1, ax=(0, 1, 0))[0]
        leaves = cmds.polyCone(name="Tree1_Leaves", radius=1, height=3, sa=10, ax=(0, 1, 0))[0]
        cmds.move(0, 2.5, 0, leaves, relative=True)
        cmds.group(trunk, leaves, name="Tree1_Group")
        
        self.assign_color(trunk, (0.55, 0.35, 0.2), "Trunk_Mat") 
        self.assign_color(leaves, (0.1, 0.5, 0.2), "Pine_Leaves_Mat")
        
    def create_tree2(self):
        """Tree2 (Blocky): Cube (Leaves) on a small Cube (Trunk)."""
        trunk = cmds.polyCube(name="Tree2_Trunk", width=0.5, height=1.5, depth=0.5)[0]
        leaves = cmds.polyCube(name="Tree2_Leaves", width=2, height=2, depth=2)[0]
        cmds.move(0, 1.75, 0, leaves, relative=True)
        cmds.group(trunk, leaves, name="Tree2_Group")
        
        self.assign_color(trunk, (0.45, 0.25, 0.1), "Trunk_Mat") 
        self.assign_color(leaves, (0.2, 0.65, 0.3), "Block_Leaves_Mat") 
        
    def create_tree3(self):
        """Tree3 (Bush): Sphere (Leaves) on a thin Cylinder (Trunk)."""
        trunk = cmds.polyCylinder(name="Tree3_Trunk", radius=0.1, height=1, sy=1, ax=(0, 1, 0))[0]
        leaves = cmds.polySphere(name="Tree3_Leaves", radius=1.5, sx=12, sy=12)[0]
        cmds.move(0, 2, 0, leaves, relative=True)
        cmds.group(trunk, leaves, name="Tree3_Group")
        
        self.assign_color(trunk, (0.6, 0.4, 0.2), "Trunk_Mat") 
        self.assign_color(leaves, (0.35, 0.7, 0.15), "Bush_Leaves_Mat") 
        
    # --- Utility Function ---
    def cleanup_existing_elements(self):
        """Deletes previous elements and custom shaders to prevent scene clutter."""
        try:
            if cmds.objExists("Ground_Plane"):
                cmds.delete("Ground_Plane")
            for i in range(1, 4):
                if cmds.objExists(f"Tree{i}_Group"):
                    cmds.delete(f"Tree{i}_Group")
            
            for shader_name in ["Ground1_Mat", "Ground2_Mat", "Ground3_Mat", "Trunk_Mat", "Pine_Leaves_Mat", "Block_Leaves_Mat", "Bush_Leaves_Mat"]:
                 if cmds.objExists(shader_name):
                     cmds.delete(shader_name)
                 if cmds.objExists(shader_name + "SG"):
                     cmds.delete(shader_name + "SG")

        except Exception as e:
            pass



def get_maya_main_window():
    """Returns the Maya main window pointer as a QWidget."""
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), QtWidgets.QWidget)


def run():
    """Initializes and shows the UI."""
    global ui
    try:
        ui.close()
    except:
        pass
    ui = ForestBuilderToolDialog(parent=get_maya_main_window())
    ui.show()

run()