
from stdcom.operatorGDRWindowGeneric import operatorGdrGeneric as ogg
import sys
import argparse

from PyQt5.QtWidgets import  QApplication

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
        window = ogg(None,nextProject)
    else:
        window = ogg()

    window.setWindowTitle("Stec GDR Operator Interfacer")

    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()
    if window.cBridge != None:
        window.cBridge.terminate()



