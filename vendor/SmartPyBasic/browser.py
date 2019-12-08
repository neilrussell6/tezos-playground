## Copyright 2019 Smart Chain Arena LLC. ##

class SmartmlCtx:
    def call(self, f, *args):
        def pp(x):
            if isinstance(x, str):
                return "'%s'" % x
            else:
                return str(x)
        #print ("  Calling %s(%s)" % (f, ', '.join(pp(x) for x in args)))
        return None

class Window:
    pythonTests = []
    smartmlCtx = SmartmlCtx()
    inBrowser = False
    contractNextId = 0
    activeTrace = None
    def nextId(self):
        result = self.contractNextId
        self.contractNextId += 1
        return result
    def cleanOutputPanel(self):
        return
    def setOutput(self, s):
        setOutput(s)

class Document:
    pass

window = Window()
document = Document()
def alert(x):
    print("ALERT" + str(x))

scenario = []
def setOutput(l):
    global scenario
    scenario = l
