from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QKeySequence

class LineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy) or event.matches(
            QKeySequence.Paste
        ):
        # or
        # if event in (QtGui.QKeySequence.Copy, QtGui.QKeySequence.Paste):
            return
        super().keyPressEvent(event)