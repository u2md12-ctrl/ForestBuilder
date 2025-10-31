try:
    from PySide6 import QtCore, QtWidgets, QtGui
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui
    from shiboken2 import wrapInstance

from project_util import ForestBuilderLogic

class ForestBuilderToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Forest Builder')
        self.resize(450, 500)

        
        self.logic = ForestBuilderLogic()

        self.setStyleSheet("""
            QDialog {
                background-image: url("C:/Users/Lenovo/Documents/maya/2024/scripts/finalproject/picture/8666420.jpg");
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.mainLayout)

        
        self.headerLabel = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("C:/Users/Lenovo/Documents/maya/2024/scripts/finalproject/picture/Treeicon.png")
        scaled_pixmap = pixmap.scaledToWidth(200, QtCore.Qt.SmoothTransformation)
        self.headerLabel.setPixmap(scaled_pixmap)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.headerLabel)

        
        self.contentFrame = QtWidgets.QFrame()
        self.contentFrame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 10px;
            }
            QLabel { font-weight: bold; }
            QComboBox, QLineEdit { background-color: white; padding: 5px; border-radius: 5px; }
        """)
        self.contentLayout = QtWidgets.QVBoxLayout()
        self.contentLayout.setContentsMargins(15, 15, 15, 15)
        self.contentLayout.setSpacing(10)
        self.contentFrame.setLayout(self.contentLayout)
        self.mainLayout.addWidget(self.contentFrame)

        
        groundLayout = QtWidgets.QHBoxLayout()
        self.GroundLabel = QtWidgets.QLabel("Ground Type:")
        self.GroundCombo = QtWidgets.QComboBox()
        self.GroundCombo.addItems(["None", "Flat Plane", "Triangle", "Circle"])
        groundLayout.addWidget(self.GroundLabel)
        groundLayout.addWidget(self.GroundCombo)
        self.contentLayout.addLayout(groundLayout)

        
        treeLayout = QtWidgets.QHBoxLayout()
        self.treeLabel = QtWidgets.QLabel("Tree Type:")
        self.treeCombo = QtWidgets.QComboBox()
        self.treeCombo.addItems(["None", "Fin Tree", "Square Tree", "Circle Tree"])
        treeLayout.addWidget(self.treeLabel)
        treeLayout.addWidget(self.treeCombo)
        self.contentLayout.addLayout(treeLayout)

        
        addTreeLayout = QtWidgets.QHBoxLayout()
        self.amountLabel = QtWidgets.QLabel("จำนวนต้นไม้:")
        self.amountInput = QtWidgets.QLineEdit("5")
        self.amountInput.setFixedWidth(60)
        self.addTreeButton = QtWidgets.QPushButton("Add Trees")
        self.addTreeButton.clicked.connect(self.add_more_trees)
        addTreeLayout.addWidget(self.amountLabel)
        addTreeLayout.addWidget(self.amountInput)
        addTreeLayout.addWidget(self.addTreeButton)
        self.contentLayout.addLayout(addTreeLayout)

        # Generate Button
        self.generateButton = QtWidgets.QPushButton("Generate")
        self.generateButton.clicked.connect(self.create_elements)
        self.contentLayout.addWidget(self.generateButton, alignment=QtCore.Qt.AlignCenter)

        # Restart Button
        self.restartButton = QtWidgets.QPushButton("Restart")
        self.restartButton.clicked.connect(self.restart_scene)
        self.contentLayout.addWidget(self.restartButton, alignment=QtCore.Qt.AlignCenter)

    
    def create_elements(self):
        self.logic.cleanup_existing_elements()
        ground_type = self.GroundCombo.currentText()
        tree_type = self.treeCombo.currentText()
        self.logic.create_ground(ground_type)
        self.logic.create_tree(tree_type)

    def add_more_trees(self):
        try:
            count = int(self.amountInput.text())
        except ValueError:
            import maya.cmds as cmds
            cmds.warning("กรุณากรอกตัวเลขจำนวนต้นไม้ที่ถูกต้อง")
            return
        tree_type = self.treeCombo.currentText()
        self.logic.add_more_trees(tree_type, count)

    def restart_scene(self):
        self.logic.cleanup_existing_elements()
        self.GroundCombo.setCurrentIndex(0)
        self.treeCombo.setCurrentIndex(0)
        self.amountInput.setText("5")
