import sys
from PyQt4 import QtGui, QtCore
import httplib2
from HTMLParser import HTMLParser
import Queue
import threading

class lists():
    visitedUrls = []
    externalUrls = []
    internalUrls = []
    webpage = ""

class MyHTMLParser(HTMLParser, lists):

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "href":
                if self.webpage.replace('http://', '') in attr[1]:
                    if attr[1] not in self.internalUrls:
                        self.internalUrls.append(attr[1])
                else:
                    if attr[1] not in self.externalUrls:
                        self.externalUrls.append(attr[1])

class mainScreen(QtGui.QWidget, lists):
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

    def updateTxtIntUrl(self, text):
        print "the text is ", text
        self.txtIntUrl.setText(str(text))

    def buttonClicked(self):
        print self.urlTxt.text()
        self.urlLbl.setText(self.urlTxt.text())
        site = self.urlTxt.text()

        self.checker = siteChecker()
        self.checker.setSite(site)
        self.connect(self.checker, QtCore.SIGNAL('txtIntUrl'), self.updateTxtIntUrl)
        self.checker.start()
        # q = Queue.Queue()
        # t = threading.Thread(target = checker.startScrape(), args = (q))
        # t.deamon = True
        # t.start()

class siteScraper(QtGui.QMainWindow, lists):
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

class siteChecker(QtCore.QThread, QtCore.QObject, lists):
    def test(self, attr):
        print "test has run", attr

    def check(self):
        h = httplib2.Http(".cache")
        h.force_exception_to_status_code = True
        resp, content = h.request(self.webpage, "GET")
        print "resp is ", resp
        parser = MyHTMLParser()
        try:
            result = parser.feed(content)
            print "the result from feed in check function is ", result
        except:
            pass
        self.visitedUrls.append(self.webpage)
        print "here are the visited sites from in the check function ", self.visitedUrls
        print "here are the internalUrls", self.internalUrls
        print "here are the externalUrls", self.externalUrls

    def setSite(self, webpage):
        self.webpage = str(webpage)

    def run(self):
        self.check()
        for self.internalUrl in self.internalUrls:
            print self.internalUrl
            print "number of urls in visited:", len(self.visitedUrls)
            print "number of internal urls:", len(self.internalUrls)
            print "number of external urls:", len(self.externalUrls)
            self.emit(QtCore.SIGNAL('txtIntUrl'), self.internalUrls)
            #self.txtIntUrl.setText("test")            

            if self.internalUrl not in self.visitedUrls:
                self.webpage = self.internalUrl
                self.check()

def main():
    app = QtGui.QApplication(sys.argv)
    scraper = siteScraper()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()