from threading import Thread


class OperationSimple:
    def __init__(self):
        self.resultAdd = 0
        self.resultSub = 0

    def add(self):
        a = 5
        b = 6
        self.returnAdd = a+b

    def sub(self):
        a = 5
        b = 6
        self.returnSub = a-b

    def getResult(self):
        print(self.resultAdd)
        print(self.resultSub)

    def updateThread(self):
        Thread(None, self.add()).start()
        Thread(None, self.sub()).start()


test = OperationSimple()
test.updateThread()
test.getResult()