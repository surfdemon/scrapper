import sys
from PyQt4 import QtGui, QtCore
import httplib2
from HTMLParser import HTMLParser

visitedUrls = []
externalUrls = []
internalUrls = []
site = ""

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global internalUrls
        global externalUrls
        global site
        for attr in attrs:
            if attr[0] == "href":
                if site in attr[1]:
                    if attr[1] not in internalUrls:
                        internalUrls.append(attr[1])
            else:
                if attr[1] not in externalUrls:
                    externalUrls.append(attr[1])

class mainScreen(QtGui.QWidget):
    def __init__(self):
        super(mainScreen, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.urlLbl = QtGui.QLabel('Site:', self)
        self.urlTxt = QtGui.QLineEdit()
        self.btnTest = QtGui.QPushButton("Button", self)
        self.txtIntUrl = QtGui.QTextEdit()
        self.txtExtUrl = QtGui.QTextEdit()
        self.txtVisitedUrl = QtGui.QTextEdit()
        self.txtExtUrl.setReadOnly(True)
        self.txtIntUrl.setReadOnly(True)
        self.txtVisitedUrl.setReadOnly(True)
        grid.addWidget(self.urlLbl,0,0)
        grid.addWidget(self.urlTxt,0,1) 
        grid.addWidget(self.btnTest,0,2)    
        grid.addWidget(self.txtExtUrl,1,0)
        grid.addWidget(self.txtIntUrl,1,1)
        grid.addWidget(self.txtVisitedUrl,2,0,1,2)

        self.setLayout(grid)
        self.btnTest.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        global internalUrls
        global externalUrls
        global visitedUrls
        global site
        print self.urlTxt.text()
        self.urlLbl.setText(self.urlTxt.text())
        site = self.urlTxt.text()
        self.check(site)
        for internalUrl in internalUrls:
            print internalUrl
            print "number of urls in visited:", len(visitedUrls)
            print "number of internal urls:", len(internalUrls)
            print "number of external urls:", len(externalUrls)
            if internalUrl not in visitedUrls:
                self.check( internalUrl)

    def check(self, webpage):
        global visitedUrls
        h = httplib2.Http(".cache")
        h.force_exception_to_status_code = True
        resp, content = h.request(str(webpage), "GET")
        parser = MyHTMLParser()
        print "site is ", site
        try:
            parser.feed(content)
        except:
            pass
        visitedUrls.append(str(webpage))
        print visitedUrls

class siteScraper(QtGui.QMainWindow):
    def __init__(self):
        super(siteScraper, self).__init__()
        self.initUI()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'message', "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def initUI(self):
        self.setCentralWidget(mainScreen())
        self.statusBar().showMessage('Ready')
        exitAction = QtGui.QAction(QtGui.QIcon(''), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu = menubar.addAction(exitAction)

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        self.setWindowTitle('Scrapper')
        self.show()

    def center(self):
        qr = self.frameGeomotry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QtGui.QApplication(sys.argv)
    scraper = siteScraper()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()