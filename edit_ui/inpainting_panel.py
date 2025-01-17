from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QRect, QBuffer, pyqtSignal
import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QPainter, QPen
from PIL import Image, ImageOps
import io

class InpaintingPanel(QWidget):
    enableScaleToggled = pyqtSignal(bool)

    def __init__(self, doInpaint, getImage, getSelection, getMask):
        super().__init__()
        assert callable(doInpaint)
        assert callable(getImage)
        assert callable(getSelection)
        assert callable(getMask)

        self.textPromptBox = QLineEdit("", self)
        self.negativePromptBox = QLineEdit("", self)

        self.batchSizeBox = QSpinBox(self)
        self.batchSizeBox.setValue(3)
        self.batchSizeBox.setRange(1, 9)
        self.batchSizeBox.setToolTip("Inpainting images generated per batch")
        self.batchCountBox = QSpinBox(self)
        self.batchCountBox.setValue(3)
        self.batchCountBox.setRange(1, 9)
        self.batchCountBox.setToolTip("Number of inpainting image batches to generate")

        self.inpaintButton = QPushButton();
        self.inpaintButton.setText("Start inpainting")
        self.inpaintButton.clicked.connect(lambda: doInpaint( getSelection(),
                    getMask(),
                    self.textPromptBox.text(),
                    self.batchSizeBox.value(),
                    self.batchCountBox.value(),
                    self.negativePromptBox.text(),
                    self.guidanceScaleBox.value(),
                    self.skipStepsBox.value()))

        self.moreOptionsBar = QHBoxLayout()
        self.guidanceScaleBox = QSpinBox(self)
        self.guidanceScaleBox.setValue(5)
        self.guidanceScaleBox.setRange(0,300)
        self.guidanceScaleBox.setToolTip("Scales how strongly the prompt and negative are considered. Higher values are more precise, but have less variation.")
        self.skipStepsBox = QSpinBox(self)
        self.skipStepsBox.setValue(0)
        self.skipStepsBox.setRange(0, 27)
        self.skipStepsBox.setToolTip("Sets how many diffusion steps to skip. Higher values generate faster and produce simpler images.")

        self.enableScaleCheckbox = QCheckBox(self)
        self.enableScaleCheckbox.setText("Scale edited areas")
        self.enableScaleCheckbox.setToolTip("Enabling scaling allows for larger sample areas and better results at small scales, but increases the time required to generate images for small areas.")
        self.enableScaleCheckbox.setChecked(True)
        self.enableScaleCheckbox.stateChanged.connect(lambda isChecked: self.enableScaleToggled.emit(isChecked))
        

        self.moreOptionsBar.addWidget(QLabel(self, text="Guidance scale:"), stretch=0)
        self.moreOptionsBar.addWidget(self.guidanceScaleBox, stretch=20)
        self.moreOptionsBar.addWidget(QLabel(self, text="Skip timesteps:"), stretch=0)
        self.moreOptionsBar.addWidget(self.skipStepsBox, stretch=20)
        self.moreOptionsBar.addWidget(self.enableScaleCheckbox, stretch=10)


        self.layout = QGridLayout()
        # Row 1 and 2:
        self.layout.addWidget(QLabel(self, text="Prompt:"), 1, 1, 1, 1)
        self.layout.addWidget(self.textPromptBox, 1, 2, 1, 1)
        self.layout.addWidget(QLabel(self, text="Negative:"), 2, 1, 1, 1)
        self.layout.addWidget(self.negativePromptBox, 2, 2, 1, 1)
        self.layout.addWidget(QLabel(self, text="Batch size:"), 1, 3, 1, 1)
        self.layout.addWidget(self.batchSizeBox, 1, 4, 1, 1)
        self.layout.addWidget(QLabel(self, text="Batch count:"), 2, 3, 1, 1)
        self.layout.addWidget(self.batchCountBox, 2, 4, 1, 1)
        self.layout.addWidget(self.inpaintButton, 2, 5, 1, 1)
        self.layout.setColumnStretch(2, 255) # Maximize prompt input

        self.layout.addLayout(self.moreOptionsBar, 3, 1, 1, 4)
        self.setLayout(self.layout)

    def scalingEnabled(self):
        return self.enableScaleCheckbox.isChecked()
