import sys, re
import argparse

from PyQt5.QtWidgets import QDialog, QApplication, QListWidgetItem, QTabWidget, QTableWidgetItem, QCheckBox, QMessageBox, QMainWindow
from PyQt5.QtCore import QSettings, QVariant, Qt, QEvent, QSize
from PyQt5.Qt import pyqtSlot, pyqtSignal

try :
    from operatorGDRWindow import *
    from stdsqlgdr import  *
    from stdcomqt5 import *
    from stdcomqt5widget import postgresConfigWidget, ipconfigDialog
except :
    from stdcom.operatorGDRWindow import *
    from stdcom.stdsqlgdr import *
    from stdcom.stdcomqt5 import *
    from stdcom.stdcomqt5widget import postgresConfigWidget, ipconfigDialog


class operatorGdrGeneric(QMainWindow):
    MultiverseHostname = "127.0.0.1"
    MultiversePort = 4897
    cBridge = None

    dbHost = "localhost"
    dbPort = 5432
    dbDbase = "vremsoft"
    dbUser = "vremsoft"
    dbPasswd = "vrem2010!"
    postgres2 = None
    multiverseDialog = None
    postgres2Dialog = None
    msg = None

    subscriptions = []


    def __init__(self, cBridge: stdcomPyQt = None, project: str = "stec-gdr"):
        """
         def __init__(self, cBridge : stdcomPyQt = None):
        :param cBridge: If you are passing a cBridge and it is controlled here, pass it else it will make one
        """

        self.project = project
        super().__init__()
        self.ui = Ui_MainWindowGdrOperator()
        self.ui.setupUi(self)
        self.project = project

        self.LoadConfig()
        self.LoadDatabase()
        self.LoadcBridge()

        self.postgres2Dialog = postgresConfigWidget(self.dbHost, str(self.dbPort), self.dbDbase, self.dbUser, self.dbPasswd, self)
        self.postgres2Dialog.OKSignal.connect(self.changePostgresParamerters)
        self.postgres2Dialog.CancelSignal.connect(self.changePostgresParamertersCancel)
        self.postgres2Dialog.hide()
        self.ui.action_Postgres.triggered.connect(self.enableConfigPostGres)

        self.multiverseDialog = ipconfigDialog(None, self.MultiverseHostname, str(self.MultiversePort))
        self.multiverseDialog.sigNewIPPort.connect(self.changecBridge)
        self.multiverseDialog.hide()
        self.ui.action_Multiverse.triggered.connect(self.enableConfigureMultiverse)
        self.ui.action_Load.triggered.connect(self.loadGrade)
        self.ui.action_Exit.triggered.connect(self.deleteLater)

        self.ui.listWidgetGrades.itemClicked.connect( self.listBoxSelected)



    def closeEvent(self, event: QEvent = None):
        """
        internal use
        :param event:
        :return:
        """
        self.postgres2Dialog.deleteLater()
        if self.cBridge is not None:
            self.cBridge.terminate()
            self.cBridge = None

        if self.multiverseDialog is not None :
            self.multiverseDialog.deleteLater()

        event.accept()


    def setostgresConnected(self, connected : True):

        if connected is True :
            self.ui.labelPostgres.setText("Postgress Connection is Made")

        else:
            self.ui.labelPostgres.setText("Postgress BROKEN Connection")


    def setcBridgeConnected(self, connected: True):

        if connected is True:
            self.ui.labelMultiverse.setText("Multiverse Connection is Made")

        else:
            self.ui.labelMultiverse.setText("Multiverse BROKEN Connection")

    @pyqtSlot(QListWidgetItem)
    def listBoxSelected(self, itm):
        text = itm.text()
        self.ui.labelGradeToLoad.setText(text)
        load = "Load: " + text
        self.ui.action_Load.setText(load)

    @pyqtSlot()
    def enableConfigPostGres(self):
        self.postgres2Dialog.show()

    @pyqtSlot()
    def enableConfigureMultiverse(self):
        self.multiverseDialog.show()

    @pyqtSlot()
    def loadGrade(self ):
        grade = self.ui.labelGradeToLoad.text()
        if grade is not None and grade == "" :
            return
        if self.postgres2.db.isOpen() :
            data = self.postgres2.getGradeInfo(grade )
            if data is not None :
                currentGradeSubscription = data.keys()
                for each in currentGradeSubscription :
                    if each  not in self.subscriptions :
                        self.subscriptions.append(each)
                        self.cBridge.subscribe(str(each))

                    d = list(data.get(each))
                    self.cBridge.writeValues(each, d)
            else:
                self.msg = QMessageBox()
                self.msg.setText("Select Grade First")
                self.msg.setInformativeText("Selection Needs to be made ")
                self.msg.setWindowTitle("Grade Selection")
                self.msg.setDetailedText("The details are as follows: You Must Select a Grade Prior To Load Attempt")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.show()
         #   msg.buttonClicked.connect(msgbtn)

    @pyqtSlot(str, str, str, str, str)
    def changePostgresParamerters(self, host, port,database,user,password ):
        self.dbHost = host
        self.dbPort = int(port)
        self.dbDbase = database
        self.dbUser = user
        self.dbPasswd = password
        self.SaveConfig()
        self.LoadDatabase()

        self.postgres2Dialog.hide()

    @pyqtSlot()
    def  changePostgresParamertersCancel(self):
        self.postgres2Dialog.hide()

    @pyqtSlot(str, str)
    def changecBridge(self, host, port):
        self.MultiverseHostname = host
        self.MultiversePort = int(port)
        self.multiverseDialog.hide()
        self.SaveConfig()
        self.LoadcBridge()

    @pyqtSlot()
    def SaveConfig(self):

        """
        Saves all setup data
        :return:
        """

        settings = VSettings(self.project)
        settings.setValue('MultiverseHostname', self.MultiverseHostname)
        settings.setValue('MultiversePort', self.MultiversePort)
        settings.setValue('PostgresHostname', self.dbHost)
        settings.setValue('PostgresPort', self.dbPort)
        settings.setValue('PostgresUser', self.dbUser)
        settings.setValue('PostgresDbase', self.dbDbase)
        settings.setValue('PostgresPasswd', self.dbPasswd)
        settings.sync()


    @pyqtSlot()
    def LoadConfig(self):
        """
        loads all configurations
        :return:
        """
        settings = VSettings(self.project)
        self.MultiverseHostname = str(settings.value("MultiverseHostname", self.MultiverseHostname))
        self.MultiversePort = int(settings.value("MultiversePort", self.MultiversePort))

        self.dbHost = str(settings.value('PostgresHostname', self.dbHost))
        self.dbPort = int(settings.value('PostgresPort', self.dbPort))
        self.dbUser = str(settings.value('PostgresUser', self.dbUser))
        self.dbDbase = str(settings.value('PostgresDbase', self.dbDbase))
        self.dbPasswd = str(settings.value('PostgresPasswd', self.dbPasswd))

    @pyqtSlot()
    def LoadcBridge(self):

        if self.cBridge is not None:
            self.cBridge.terminate()

        else:
            self.cBridge = stdcomPyQt(self)
            self.cBridge.sigConnect.connect(self.cBridgeConnected)

        self.setcBridgeConnected(False)
        self.cBridge.setDestination(self.MultiverseHostname, self.MultiversePort)
        self.cBridge.LoadcBridge()


    @pyqtSlot()
    def cBridgeConnected(self):
        self.setcBridgeConnected(True)


    @pyqtSlot()
    def LoadDatabase(self):
        """
        load the database, this is set to a postgres database
        """
        self.setostgresConnected(False)
        if self.postgres2 is not None:
            self.postgres2.closeDb()
            self.postgres2.deleteLater()

        self.postgres2 = stdsqlgdr(self.dbUser, self.dbDbase, self.dbHost, self.dbPort, self.dbPasswd)
        if self.postgres2.db.isOpen() :
            self.setostgresConnected(True)

            grades = self.postgres2.loadGrades()
            self.ui.listWidgetGrades.clear()

            for i in range(0,len(grades)):
                self.ui.listWidgetGrades.insertItem(i, grades[i] )

        else:
            self.msg = QMessageBox()
            self.msg.setText("Postgress Connection Not Made")
            self.msg.setInformativeText("Selection Needs to be made ")
            self.msg.setWindowTitle("Recheck Postgres Parameters")
            self.msg.setDetailedText("The details are as follows: You Must Select Correct Parameters for the Postgres Database")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()



if __name__ == "__main__":
    """
    bumped version
    """

    my_parser = argparse.ArgumentParser( description="Version 1.6.04 Stec Python Version")
    # Add the arguments
    my_parser.add_argument('-p','--project', metavar='project', required=False)


    args = my_parser.parse_args()
    nextProject = args.project

    app = QApplication(sys.argv)
    if nextProject is not None :
        window = operatorGdrGeneric(None,nextProject)
    else:
        window = operatorGdrGeneric()

    window.setWindowTitle("Stec GDR Operator Interfacer")

    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()
    if window.cBridge != None:
        window.cBridge.terminate()


