import sys, re
import argparse

try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None


from PyQt5.QtWidgets import QDialog, QApplication, QTabWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import QSettings, QVariant, Qt, QEvent
from PyQt5.Qt import pyqtSlot, pyqtSignal

try :
    from pjanicesimple import *
    from stdcomqt5 import *
    from stdcomqt5widget import *
except :
    from stdcom.pjanicesimple import *
    from stdcom.stdcomqt5 import *
    from stdcom.stdcomqt5widget import *

class pjanicesimpleGeneric(QDialog):
    """
    Stec Pjanice Widget, but with trees not list.
    """

    sigSelectedData = pyqtSignal(str, list)

    selected = False
    cBridge = None
    currentSub = ""

    data = []

    suspectTable = False
    liveSubscriptions = {"": []}


    alternativeIgnore = None


    def __init__(self, cBridge: stdcomPyQt,  parent = None):


        super().__init__(parent)
        self.ui = Ui_pJaniceSimple()
        self.ui.setupUi(self)
        self.cBridge = cBridge
        self.show()

        tags = cBridge.getPossibleSubscribers()

        if tags is None or len(tags) == 0 :
            tags = ["Stec"]

        self.treeViewTags = stdcomqt5qtreeMorph(self.ui.treeWidgetUI, tags, self)
        self.treeViewTags.newTextSignal.connect(self.slotSelected)

        self.cBridge.sigNames.connect(self.slotNames)
        self.cBridge.sigNewData.connect(self.slotNewData)
        self.cBridge.sigNewDesc.connect(self.slotDesc)

        self.ui.tableWidgetData.itemChanged.connect(self.on_any_itemChanged)
        self.alternativeIgnore = None


    def setAlternativeIgnore(self, function=None):
        """
        set the alternative callback
        """
        self.alternativeIgnore = function;

    def areOtherUsingSub(self, name: str):
        """
        return users callback if there
        """
        if self.alternativeIgnore is not None:
            return self.alternativeIgnore(name)

        return False

    def getcBridge(self):
        """
        return the current cBridge, the stdcomPyQt which is the qt version of the stdcom
        """
        return self.cBridge

    @pyqtSlot(str, str)
    def slotDesc(self, name, desc):
        """
        internal use
        """
        self.treeViewTags.AddDesc(name, desc)
        if name == self.currentSub:
            self.ui.plainTextEditDesc.clear()
            self.ui.plainTextEditDesc.insertPlainText(desc)

    @pyqtSlot(list)
    def slotNames(self, names):
        """
        internal use
        """
        self.treeViewTags.AddNames(names)

    @pyqtSlot(str, str)
    def slotSelected(self, name, desc):
        """
        selected slot, it tree item is clicked
        """
        self.ui.tableWidgetData.clear()
        if self.currentSub != "":
            if self.areOtherUsingSub(name) is False:
                self.cBridge.unsubscribe(self.currentSub)

        self.currentSub = name
        self.cBridge.subscribe(name)
        self.selected = False

        self.ui.lineEditTag.setText(name)
        self.ui.plainTextEditDesc.clear()
        if desc != "":
            self.ui.plainTextEditDesc.insertPlainText(desc)

        self.cBridge.getPossibleSubscribers()
        values = self.cBridge.readValues(name)
        if values is not None and len(values):
            self.slotNewData(name, values)

    @pyqtSlot(str, list)
    def slotNewData(self, name, data):
        """
        data as it comes in from Multiverse
        :param name:
        :param data:
        :return:
        """
        if name == self.currentSub:
            self.ui.tableWidgetData.clear()
            self.ui.tableWidgetData.setRowCount(len(data))
            self.ui.tableWidgetData.setColumnCount(1)

            self.suspectTable = True
            self.data = data
            for i in range(0, len(data)):
                d = QTableWidgetItem(str(data[i]))
                self.ui.tableWidgetData.setItem(i, 0, d)

            self.suspectTable = False
            if self.selected == False:
                self.sigSelectedData.emit(name, data)
                self.selected = True


    @pyqtSlot()
    def Reset(self):
        self.treeViewTags.clear()
        self.ui.lineEditTag.clear()

        self.data = []
        self.liveSubscriptions = {"": []}


    def ResetClear(self, host : str = None,  port : str = None):
        if host is not None and port is not None :
            self.cBridge.terminate()
            self.cBridge.setDestination(host, port)
            self.cBridge.LoadcBridge()

        self.treeViewTags.clear()
        self.ui.lineEditTag.clear()

    @pyqtSlot(QTableWidgetItem)
    def on_any_itemChanged(self, itm: QTableWidgetItem):
        """
        when any item is clicked
        """
        c = itm.column()
        r = itm.row()

        if self.suspectTable is False:
            print("Changed R/C ", r, "/", c, itm.text())
            if r < len(self.data):
                self.data[r] = itm.text()
                self.cBridge.writeValues(self.currentSub, self.data)

    @pyqtSlot()
    def addRow(self):
        """
        adds a row to table
        """
        rows = self.ui.tableWidgetLiveTags.rowCount()
        self.ui.tableWidgetLiveTags.setRowCount(rows + 1)




if __name__ == "__main__":
    """
    bumped version
    """

    my_parser = argparse.ArgumentParser( description="Version 1.6.04 Stec Pjanice Python Version")
    # Add the arguments
    my_parser.add_argument('-p','--project', metavar='project', required=False)

    cBridge = stdcomPyQt()
    cBridge.setDestination("127.0.0.1", "4897")
    cBridge.LoadcBridge()


    args = my_parser.parse_args()
    nextProject = args.project


    app = QApplication(sys.argv)

    window = pjanicesimpleGeneric(cBridge)


    window.setWindowTitle("Stec PJanice Viewer")

    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()
    if window.cBridge != None:
        window.cBridge.terminate()
