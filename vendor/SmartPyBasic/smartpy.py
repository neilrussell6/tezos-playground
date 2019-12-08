## Copyright 2019 Smart Chain Arena LLC. ##

import inspect
import sys
import traceback

import vendor.SmartPyBasic.smartpyio as smartpyio
from vendor.SmartPyBasic.browser import alert, window

pyRange = range
pyBool  = bool
pyInt   = int
pySet   = set
pyList  = list
pyTuple = tuple
pyBytes = bytes
pyMap   = map

class Expr:
    def __init__(self, f, l):
        self._f = f
        self._l = l
        self.onUpdateHandlers = []
        self.attributes = {}
        self.opens = {}
        setattr(self, '__initialized', True)

    def __eq__       (self, other): return Expr("eq",       [self, spExpr(other)])
    def __ne__       (self, other): return Expr("ne",       [self, spExpr(other)])
    def __add__      (self, other): return Expr("add",      [self, spExpr(other)])
    def __sub__      (self, other): return Expr("sub",      [self, spExpr(other)])
    def __mul__      (self, other): return Expr("mul",      [self, spExpr(other)])
    def __mod__      (self, other): return Expr("mod",      [self, spExpr(other)])
    def __truediv__  (self, other): return Expr("truediv",  [self, spExpr(other)])
    def __floordiv__ (self, other): return Expr("floordiv", [self, spExpr(other)])

    def __radd__     (self, other): return Expr("add",      [spExpr(other), self])
    def __rmul__     (self, other): return Expr("mul",      [spExpr(other), self])
    def __rsub__     (self, other): return Expr("sub",      [spExpr(other), self])

    def __lt__       (self, other): return Expr("lt",       [self, spExpr(other)])
    def __le__       (self, other): return Expr("le",       [self, spExpr(other)])
    def __gt__       (self, other): return Expr("gt",       [self, spExpr(other)])
    def __ge__       (self, other): return Expr("ge",       [self, spExpr(other)])
    def __or__       (self, other): return Expr("or",       [self, spExpr(other)])
    def __and__      (self, other): return Expr("and",      [self, spExpr(other)])

    def __getitem__  (self, item ): return Expr("getItem",  [self, spExpr(item)])

    def __abs__      (self):        return Expr("abs",      [self])
    def __neg__      (self):        return Expr("neg",      [self])
    def __invert__   (self):        return Expr("invert",   [self])

    def __bool__     (self): self.__nonzero__()
    def __nonzero__  (self): raise Exception("Cannot convert expression to bool. Conditionals are forbidden on contract expressions. Please use ~ or sp.if instead of not or if.")

    def __hash__(self):
        return hash(self.export())
    def onUpdate(self, f):
        self.onUpdateHandlers.append(f)
    def get(self, item, defaultValue = None):
        if defaultValue is not None:
            return Expr("getItemDefault", [self, spExpr(item), spExpr(defaultValue)])
        return self.__getitem__(item)
    def __enter__(self):
        return getattr(self, '__asBlock').__enter__()
    def __exit__(self, type, value, traceback):
        getattr(self, '__asBlock').__exit__(type, value, traceback)
    def __iter__(self):
        raise Exception("Please use [sp.for var in expr] or [expr.items()] to iterate on a SmartPy expression.")
    def contains(self, value):
        return Expr("contains", [self, spExpr(value)])
    def __contains__(self, value):
        raise Exception("Instead of using expressions such as e1 in e2, please use e2.contains(e1).")
    def __call__(self, *args):
        raise Exception("Expression [%s] cannot be called" % str(self))
    def __getattr__(self, attr):
        if "__" in attr:
            raise AttributeError("")
        try:
            return self.attributes[attr]
        except KeyError:
            result = Expr("attr", [self, attr])
            self.attributes[attr] = result
            return result
    def __setattr__(self, attr, value):
        if '__' not in attr and hasattr(self, '__initialized'):
            sp.set(getattr(self, attr), value)
            if hasattr(getattr(self, attr), 'onUpdateHandlers') and getattr(self, attr).onUpdateHandlers:
                for f in getattr(self, attr).onUpdateHandlers:
                    f(getattr(self, attr), value)
        else:
            object.__setattr__(self, attr, value)
    def __delitem__(self, item):
        sp.delItem(self, item)
    def __setitem__(self, item, value):
        sp.set(self[item], value)
    def items(self):
        return Expr("items", [self])
    def keys(self):
        return Expr("keys", [self])
    def values(self):
        return Expr("values", [self])
    def elements(self):
        return Expr("elements", [self])
    def set(self, other):
        sp.set(self, spExpr(other))
    def add(self, item):
        sp.updateSet(self, item, True)
    def remove(self, item):
        sp.updateSet(self, item, False)
    def __repr__(self):
        return self.export()
    def isSome(self):
        return self.isVariant("Some")
    def isVariant(self, name):
        return Expr("isVariant", [self, name])
    def openSome(self):
        return self.openVariant("Some")
    def openVariant(self, name):
        try:
            return self.opens[name]
        except KeyError:
            result = Expr("openVariant", [self, name])
            self.opens[name] = result
            return result
    def append(self, other):
        raise Exception("myList.append(..) is deprecated. Please use myList.push(..).\nBeware: push adds the element in front of the list (as in Michelson).")
    def push(self, other):
        return sp.set(self, sp.cons(self, spExpr(other)))
    def addSeconds(self, seconds):
        return Expr("addSeconds", [self, spExpr(seconds)])
    def export(self):
        def ppe(e):
            if hasattr(e, "export"):
                return e.export()
            if isinstance(e, str):
                return '"%s"' % e
            return str(e)
        if self._l:
            return "(%s %s)" % (self._f, " ".join(ppe(x) for x in self._l))
        return "(%s)" % (self._f)

def literal(t, l): return Expr("literal", [ Expr(t, [l]) ])

def hashed(s): return literal("hashed", s)

unit = Expr("unit", [])
def bool(x)            : return literal("bool", x)
def int(x)             : return literal("int", x)
def nat(x)             : return literal("nat", x)
def string(x)          : return literal("string", x)
def bytes(x)           : return literal("bytes", x)
none = Expr("None", [])
def some(x)            : return Expr("variant", ["Some", spExpr(x)])
def mutez(x)           : return literal("mutez", x) if isinstance(x, pyInt) else splitTokens(mutez(1), x, 1)
def timestamp(seconds) : return literal("timestamp", seconds)
def address(s)         :
    if s == "":
        raise Exception('"" is not a valid address')
    if not (any(s.startswith(prefix) for prefix in ['KT1', 'tz1', 'tz2', 'tz3'])):
        raise Exception('"%s" is not a valid address, it should start with tz1, tz2, tz3 or KT1.' % s)
    return literal("address", s)
def key(s)             : return literal("key", s)
def signature(sig)     : return literal("signature", sig)
def hashKey(x)         : return hashed(window.smartmlCtx.call("hashString", x)) if isinstance(x, str) else Expr("hash", [x])

def tez(x): return literal("mutez", 1000000 * x) if isinstance(x, pyInt) else splitTokens(tez(1), x, 1)

def spExpr(x):
    debug = False #isinstance(x, dict)
    if isinstance(x, Expr):
        if debug: alert('Expr')
        return x
    if x == ():
        if debug: alert('unit')
        return unit
    if isinstance(x, float):
        if debug: alert('float')
        return literal("float", x)
    if isinstance(x, pyBool):
        if debug: alert('bool')
        return literal("bool", x)
    if isinstance(x, pyInt):
        if debug: alert('int')
        if x < 0:
            return literal("int", x)
        return literal("intOrNat", x)
    if isinstance(x, SmartmlValue):
        if debug: alert('SmartmlValue')
        return x
    if hasattr(x, "__int__"):
        return literal("intOrNat", pyInt(x))
    if isinstance(x, str):
        if debug: alert('str')
        return literal("string", x)
    if isinstance(x, pyBytes):
        if debug: alert('bytes')
        return literal("bytes", x.decode())
    if isinstance(x, TRecord):
        if debug: alert('TRecord')
        return literal("record", x)
    if isinstance(x, TList):
        if debug: alert('TList')
        return literal("list", x)
    if isinstance(x, WouldBeValue):
        if debug: alert('WouldBeValue')
        return x
    if isinstance(x, dict):
        if debug: alert('dict')
        return map(x)
    if isinstance(x, pySet):
        if any(isinstance(y, Expr) for y in x):
            raise Exception("{e1, ..., en} syntax is forbidden for SmartPy Expr. Please use sp.set([e1, .., en])")
        return set([spExpr(y) for y in x])
    if isinstance(x, pyTuple):
        if debug: alert('tuple')
        return tuple([spExpr(y) for y in x])
    if isinstance(x, pyList):
        if debug: alert('list')
        return list([spExpr(y) for y in x])
    if isinstance(x, pyRange):
        if debug: alert(x); alert('range')
        return list(pyList(x))
    raise Exception("spExpr: '%s' of type '%s'" % (str(x), str(type(x))))

class TType: pass

class TRecord(TType):
    def __init__(self, **kargs):
        args = sorted(kargs.items())
        self.kargs = kargs
        for (k, v) in args:
            setattr(self, k, sp.types.conv(v))
    def export(self):
        return "(record %s)" % " ".join("(%s %s)" % (x, y.export()) for (x, y) in sorted(self.kargs.items()))

class TSimple(TType):
    def __init__(self, name):
        self.name = name
    def export(self):
        return '"%s"' % self.name

TUnit      = TSimple("unit")
TBool      = TSimple("bool")
TInt       = TSimple("int")
TNat       = TSimple("nat")
TIntOrNat  = TSimple("intOrNat")
TString    = TSimple("string")
TBytes     = TSimple("bytes")
TMutez     = TSimple("mutez")
TTimestamp = TSimple("timestamp")
TAddress   = TSimple("address")
TKey       = TSimple("key")
TKeyHash   = TSimple("hash")
TSignature = TSimple("signature")

class TUnknown(TType):
    def __init__(self, id=""):
        self.id = id
    def export(self):
        return "(unknown \"%s\")" % self.id

class TList(TType):
    def __init__(self, t):
        self.t = t
    def export(self):
        return "(list %s)" % self.t.export()

class TMap(TType):
    def __init__(self, k, v):
        self.k = k
        self.v = v
    def export(self):
        return "(map %s %s)" % (sp.types.conv(self.k).export(), sp.types.conv(self.v).export())

class TSet(TType):
    def __init__(self, t):
        self.t = t
    def export(self):
        return "(set %s)" % (sp.types.conv(self.t).export())

class TBigMap(TType):
    def __init__(self, k, v):
        self.k = k
        self.v = v
    def export(self):
        return "(bigmap %s %s)" % (sp.types.conv(self.k).export(), sp.types.conv(self.v).export())

class TPair(TType):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def export(self):
        return "(pair %s %s)" % (sp.types.conv(self.t1).export(), sp.types.conv(self.t2).export())

class TAnnots(TType):
    def __init__(self, t, *annots):
        self.t = t
        self.annots = annots
    def export(self):
        return "(annots %s (%s))" % (sp.types.conv(self.t).export(), ' '.join('"%s"' % a for a in self.annots))

class TOption(TType):
    def __init__(self, t):
        self.t = t
    def export(self):
        return "(option %s)" % sp.types.conv(self.t).export()

class TContract(TType):
    def __init__(self, t):
        self.t = t
    def export(self):
        return "(contract %s)" % sp.types.conv(self.t).export()

class SpTypes:
    def __init__(self):
        self.unknownIds = 0
    def conv(self, t):
        if t is None:
            t = self.unknown()
        if t == pyInt:
            raise Exception("Type int in this context is referred to as sp.TInt.")
        if t == pyBool:
            raise Exception("Type bool in this context is referred to as sp.TBool.")
        if t == str:
            raise Exception("Type str in this context is referred to as sp.TString.")
        #
        # if t == pyBytes:
        #     raise Exception("Type bytes in this context is referred to as sp.TBytes.")
        #
        # Commented out because in Brython the following line raises an exception:
        # print(TUnknown("x") == pyBytes)
        # This is most likely a Brython bug.
        #
        if isinstance(t, pyList) and len(t) == 1:
            return TList(self.conv(t[0]))
        if isinstance(t, TType) or isinstance(t, Expr):
            return t
        raise Exception("Bad type expression " + str(t))
    def trecord(self, **kargs):
        for x in kargs:
            kargs[x] = self.conv(kargs[x])
        return TRecord(kargs)
    def unknown(self, name = ""):
        self.unknownIds += 1
        return TUnknown("%s %i" % (name, self.unknownIds))
    def taddress(self):
        return TAddress
    def tlist(self, t):
        return TList(t)

class Data:
    def __getattr__(self, attr):
        if "__" in attr:
            raise AttributeError("")
        return Expr("attr", [Expr("data", []), attr])
    def __setattr__(self, attr, value):
        sp.set(getattr(self, attr), value)

class TreeBlock:
    def __init__(self):
        self.commands = []
        self.locals = []
    def append(self, command):
        self.commands.append(command)
    def addLocal(self, var):
        self.locals.append(var)
    def export(self):
        return "(%s %s)" % (' '.join(x.export() for x in self.commands), ' '.join('(deleteLocal "%s")' % x for x in self.locals))

class CommandBlock:
    def __init__(self, sp):
        self.sp = sp
        self.commands = TreeBlock()
        self.value = None
    def __enter__(self):
        self.currentBlock = self.sp.mb.currentBlock
        self.sp.mb.currentBlock = self.commands
        return self.value
    def __exit__(self, type, value, traceback):
        self.sp.mb.currentBlock = self.currentBlock
    def export(self):
        return self.commands.export()

class Sp:
    def __init__(self):
        self.types         = SpTypes()
        self.profiling     = False
        self.profilingLogs = []
    def setLineNumber(self, linenb):
        self.newCommand(Expr("linenb", [linenb]))
    def profile(self, s = ""):
        if self.profiling:
            import datetime
            self.profilingLogs.append(str(datetime.datetime.now()) + " " + s)
    def setMB(self, mb):
        self.mb = mb
    def set(self, *args):
        self.mb.set(*args)
    def delItem(self, expr, item):
        if not window.inBrowser:
            lineno = -1
        else:
            lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-4][1], '$line_info').split(',')[0])
        self.newCommand(Expr("delItem", [expr, spExpr(item), lineno]))
    def cons(self, t, x):
        return Expr("cons", [spExpr(t), spExpr(x)])
    def newCommand(self, command):
        if hasattr(self, 'mb') and self.mb is not None:
            self.mb.append(command)
    def set(self, var, value):
        if not window.inBrowser:
            lineno = -1
        else:
            lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-4][1], '$line_info').split(',')[0])
        sp.setLineNumber(lineno)
        if value is None:
            raise Exception("None value for ", var)
        self.newCommand(Expr("set", [var, spExpr(value)]))
    def updateSet(self, set, item, add):
        if not window.inBrowser:
            lineno = -1
        else:
            lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-4][1], '$line_info').split(',')[0])
        self.newCommand(Expr("updateSet", [spExpr(set), spExpr(item), add, lineno]))
    def newLocal(self, name, value, t):
        if t == "UNKNOWN":
            t = sp.types.unknown("local %s" % name)
        t = sp.types.conv(t)
        self.defineLocal(name, spExpr(value), t)
        return Expr("getLocal", [name, t])
    def defineLocal(self, name, value, t):
        self.newCommand(Expr("defineLocal", [name, value, t]))
        self.mb.addLocal(name)
    def getData(self):
        return Expr("data", [])

sp = Sp()

class MessageBuilder:
    def __init__(self, addedMessage):
        self.name         = addedMessage.name
        self.addedMessage = addedMessage
        self.commands     = TreeBlock()
        self.currentBlock = self.commands
    def newBlock(self, b):
        self.currentBlock.append(b)
    def closeBlock(self):
        del self.currentBlock[-1]
    def append(self, command):
        self.currentBlock.append(command)
    def addLocal(self, var):
        self.currentBlock.addLocal(var)
    def export(self):
        return self.commands.export()
    def __repr__(self):
        return "Commands:%s" % (' '.join(str(command) for command in self.commands))
    def pp(self):
        output = ["    " + (command.pp()) for command in self.commands]
        return "\n".join(outputs)

class ExecutedMessage:
    def __init__(self, title, result, expected):
        self.title    = title
        self.result   = result
        self.expected = expected
    def html(self):
        return ("" if self.expected else "<br><span class='partialType'>ERROR: Unexpected result</span> please use .run(valid = ..expected validation..)<br>") + self.result
    def __repr__(self):
        return self.html()

class PreparedMessage:
    def __init__(self):
        pass
    def html(self):
        data = {}
        data['action']       = 'message'
        data['id']           = self.contractId
        data['message']      = self.message
        data['params']       = self.params
        data['lineNb']       = self.lineNb
        data['title']        = self.title
        data['messageClass'] = self.messageClass
        data['sender']       = self.sender
        data['time']         = self.time
        data['amount']       = self.amount
        data['show']         = True
        data['valid']        = self.valid
        return [data]

class ExecMessage:
    def __init__(self, _contract, _message, params, kargs):
        self.message = _message
        self.params = None if params is None else spExpr(params)
        self.kargs = None if kargs is None else { k : spExpr(v) for (k, v) in kargs.items() }
        if params is not None and kargs:
            raise Exception("Message execution uses either one args or *kargs syntax, not both.")
        self.contract = _contract
        self.smartml = _contract.smartml
        if window.inBrowser:
            self.lineNb = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-4][1], '$line_info').split(',')[0])
        else:
            self.lineNb = -1
    def html(self):
        return self.run().html()
    def run(self, sender = "", amount = mutez(0), now = None, valid = True):
        if isinstance(now, Expr) and now._f == "literal":
            now = now._l[0]
        if isinstance(sender, Expr) and sender._f == "literal":
            sender = sender._l[0]
        if isinstance(sender, Expr) and sender._f == "address":
            sender = sender._l[0]
        if not isinstance(sender, str):
            raise Exception("Sender should be of type string or address" + str(sender))
        if isinstance(amount, pyInt):
            raise Exception("Amount should be in tez or mutez and not int (use sp.tez(..) or sp.mutez(..))")
        if isinstance(now, Expr) and now._f == "timestamp":
            now = now._l[0]
        if now is not None:
            if not isinstance(now, pyInt):
                raise Exception("bad now " + str(now))
            self.smartml.setNow(now)
        sp.profile(self.message + " begin")

        if self.params is None:
            self.params = record(**self.kargs)
        sp.profile(self.message + " params")
        if window.inBrowser:
            if window.activeScenario is not None:
                scenario = window.activeScenario
                expr = scenario.smartml.importExpr(self.params)
                contracts = scenario.allContracts()
                self.params = scenario.smartml.evalExprWithContracts(expr)
            else:
                self.params = self.smartml.importValue(self.params)
            result = self.smartml.ctx.call("execMessage", self.lineNb, self.contract.title, self.contract.execMessageClass, sender, self.smartml.time, amount.export(), self.smartml.contract, self.message, self.params)
            sp.profile(self.message + " call")
            ok = result[1] # self.smartml.messageOK(result)
            if ok:
                self.smartml.contract = result[2][1] # self.smartml.messageContract(result) # result[2][1] #
                self.contract.data = SmartmlValue(self.smartml, result[6]) # self.contract.getData()
                if window.activeScenario is not None:
                    self.contract.data = Expr("contractData", [self.smartml.contractId])
            html = result[5] # self.smartml.messageHtml(result)
            validOk = ok == valid
            result = ExecutedMessage(self.contract.title, html, validOk)
            if not validOk:
                window.validityErrors.append(str(self.lineNb))
            sp.profile(self.message + " end")
            return result
        else:
            self.params = self.smartml.importValue(self.params)
            self.contract.data = Expr("contractData", [self.smartml.contractId])
            result = PreparedMessage()
            result.lineNb       = self.lineNb
            result.title        = self.contract.title
            result.messageClass = self.contract.execMessageClass
            result.sender       = sender
            result.time         = self.smartml.time
            result.amount       = amount.export()
            result.contractId   = self.smartml.contractId
            result.message      = self.message
            result.params       = self.params
            result.valid        = valid
            return result

def unknownTypeParam(t, s):
    if t == "UNKNOWN":
        t = sp.types.unknown(s)
    t = sp.types.conv(t)
    return t

class WouldBeValue:
    def html(self, **kargs):
        return self.asValue().html(**kargs)
    def asValue(self):
        smartml = Smartml()
        return SmartmlValue(smartml, smartml.importValue(self))

class SmartmlValue:
    def __init__(self, smartml, v):
        self.smartml = smartml
        self.v       = v
        setattr(self, '__initialized', True)
    def go(self, name):
        result = self.smartml.ctx.call('go_value', self.v, name)
        return SmartmlValue(self.smartml, result)
    def export(self):
        return self.smartml.ctx.call('export_value', self.v)
    def __iter__(self):
        return iter(self.smartml.expandList(self.smartml.list_of_value(self.v)))
    def __getitem__(self, item):
        return self.smartml.getItem(self.v, self.smartml.importValue(spExpr(item)))
    def __repr__(self):
        return self.smartml.ctx.call('string_of_value', self.v)
    def __int__(self):
        return self.smartml.ctx.call('int_of_value', self.v)
    def __bool__(self):
        return True == self.smartml.ctx.call('bool_of_value', self.v) # To ensure the representation is correct, else we have 0 or 1.
    def html(self, stripStrings = False):
        return self.smartml.ctx.call('html_of_value', self.v, stripStrings)
    def __getattr__(self, attr):
        if "__" in attr:
            alert("Error while trying to get %s on SmartML value %s" % (attr, str(self)))
            raise AttributeError("")
        return self.go(attr)

class record(WouldBeValue):
    def __init__(self, **fields):
        self.fields = { k : spExpr(v) for (k, v) in fields.items() }
        for (k, v) in self.fields.items():
            setattr(self, k, v)
    def export(self):
        return "(record %s)" % (" ".join("(%s %s)" % (k, v.export()) for (k, v) in sorted(self.fields.items())))
    def __repr__(self):
        return self.export()

class tuple(WouldBeValue):
    def __init__(self, l = []):
        self.l = l
    def export(self):
        return "(tuple %s)" % (" ".join(spExpr(x).export() for x in self.l))

def pair(e1, e2):
    return tuple([e1, e2])

class list(WouldBeValue):
    def __init__(self, l = [], t = "UNKNOWN"):
        self.t = unknownTypeParam(t, "list t")
        self.l = l
    def export(self):
        return "(list %s %s)" % (self.t.export(), " ".join(spExpr(x).export() for x in self.l))

class set(WouldBeValue):
    def __init__(self, l = [], t = "UNKNOWN"):
        self.t = unknownTypeParam(t, "set t")
        self.l = l
    def export(self):
        return "(set %s %s)" % (self.t.export(), " ".join(spExpr(x).export() for x in self.l))

class map(WouldBeValue):
    def name(self):
        return "map"
    def __init__(self, l = {}, tkey = "UNKNOWN", tvalue = "UNKNOWN"):
        self.tkey = unknownTypeParam(tkey, "%s tkey" % self.name())
        self.tvalue = unknownTypeParam(tvalue, "%s tvalue" % self.name())
        self.l = l
    def export(self):
        return "(%s %s %s %s)" % (self.name(), self.tkey.export(), self.tvalue.export(),
                                   " ".join("(%s %s)" % (spExpr(k).export(), spExpr(v).export()) for (k, v) in self.l.items()))

class bigMap(map):
    def name(self):
        return "big_map"

class Smartml:
    def __init__(self, contract = None):
        self.ctx  = window.smartmlCtx
        self.time = 0
        if contract is not None:
            sp.profile("smartml linking")
            contract = contract.export()
            sp.profile("smartml export")
            self.contractId = window.nextId()
            window.contracts[self.contractId] = self
            if window.inBrowser:
                self.contract = self.ctx.call('importContract', contract)
            else:
                self.contract = contract
            sp.profile("smartml link")
    def smartpy(self):
        return self.ctx.call('string_of_contract', self.contract)
    def string_of_value(self, s):
        return self.ctx.call('string_of_value', s)
    def string_of_expr(self, s):
        return self.ctx.call('string_of_expr', s)
    def html_of_value(self, s):
        return self.ctx.call('html_of_value', s)
    def html(self):
        return self.ctx.call("htmlContract", self.contract)
    def fullHtml(self, default = "SmartPy", onlyDefault = False):
        if window.inBrowser:
            return self.ctx.call("Contract.full_html", self.contract, default, onlyDefault)
        else:
            data = {}
            data['action'] = 'newContract'
            data['id']     = self.contractId
            data['export'] = self.contract
            data['show']   = True
            return [data]
    def simulation(self, linenb):
        return self.ctx.call("simulation", self.contract, linenb)
    def messageEffects(self, result):
        return self.ctx.call("messageEffects", result)
    def messageHtml(self, result):
        return self.ctx.call("messageHtml", result)
    def messageErrors(self, result):
        return self.ctx.call("messageErrors", result)
    def messageOK(self, result):
        return self.ctx.call("messageOK", result)
    def messageContract(self, message):
        return self.ctx.call("messageContract", message)
    def list_of_value(self, value):
        return self.ctx.call("list_of_value", value)
    def getItem(self, value, item):
        return SmartmlValue(self, self.ctx.call("getItem", value, item))
    def listLength(self, l):
        return self.ctx.call("List.length", l)
    def listNth(self, l, n):
        return SmartmlValue(self, self.ctx.call("List.nth", l, n))
    def list_to_ocaml(self, l):
        result = self.ctx.call("list.[]")
        for x in reversed([x for x in l]):
            result = self.ctx.call("list.append", x, result)
        return result
    def expandList(self, l):
        r = pyRange(0, self.listLength(l))
        return [self.listNth(l, i) for i in r]
    def ocamlString(self, s):
        return self.ctx.call("string", s)
    def of_ocamlString(self, s):
        return self.ctx.call("of_ocamlString", s)
    def pair(self, l1, l2):
        return self.ctx.call("pair", l1, l2)
    def list_empty(self):
        return self.ctx.call("list.[]")
    def list_unit(self, x):
        return self.ctx.call("list.unit", x)
    def list_concat(self, l1, l2):
        return self.ctx.call("list.concat", l1, l2)
    def callImportValue(self, s):
        if window.inBrowser:
            return self.ctx.call("importValue", s)
        else:
            return s
    def importExpr(self, expr):
        return self.ctx.call("importExpr", expr.export())
    def evalExpr(self, contracts, expr):
        return self.ctx.call("evalExpr", contracts, expr)
    def evalExprWithContracts(self, expr):
        return self.ctx.call("evalExprWithContracts", expr)
    def emptyContractMap(self):
        return self.ctx.call("emptyContractMap")
    def addContract(self, key, value, hashtbl):
        self.ctx.call("addContract", key, value, hashtbl)
    def importValue(self, value):
        if isinstance(value, SmartmlValue):
            return value.v
        if isinstance(value, str):
            return self.callImportValue('(string "%s")' % value) ## TODO escaping
        if isinstance(value, pyBytes):
            return self.callImportValue('(bytes "%s")' % value) ## TODO escaping
        if isinstance(value, pyBool):
            return self.callImportValue("(bool %s)" % str(value))
        if isinstance(value, pyInt):
            return self.callImportValue("(int %i)" % value)
        if hasattr(value, "export"):
            return self.callImportValue(value.export())
        raise Exception("Unsupported type for value %s of type %s" % (str(value), str(type(value))))
    def getStorageValue(self):
        return SmartmlValue(self, self.ctx.call("getStorageValue", self.contract))
    def setNow(self, time):
        self.time = time
        return "Setting time to [%s].<br>" % time
    def ppMich(self, mich, indent = ""):
        return self.ctx.call("mich.pp", indent, mich)
    def ppMichStorage(self, mich, indent = ""):
        return self.ctx.call("mich.ppStorage", indent, mich)
    def ppMessageBuilder(self, storage, st, pt, code):
        self.ctx.call("mich.messageBuilder", storage, st, pt, code)
    def ppMichInfos(self, address, balance, manager):
        self.ctx.call("mich.htmlInfos", address, balance, manager)
    def ppMichStorageType(self, storageType):
        return self.ctx.call("mich.htmlType", storageType)
    def parseMich(self, code):
        if isinstance(code, str):
            return self.ctx.call("mich.string", code)
        if hasattr(code, 'int'):
            return self.ctx.call("mich.int", code.int)
        if hasattr(code, 'string'):
            return self.ctx.call("mich.string", code.string)
        if not hasattr(code, 'prim'):
            seq = [self.parseMich(sub) for sub in code]
            seq = self.list_to_ocaml(seq)
            return self.ctx.call("mich.sequence", seq)
        if hasattr(code, 'args'):
            args = [self.parseMich(arg) for arg in code.args]
        else:
            args = []
        argsML = self.list_to_ocaml(args)
        if hasattr(code, 'annots'):
            annots = code.annots
        else:
            annots = []
        annots = self.list_to_ocaml([self.ocamlString(x) for x in annots])
        return self.ctx.call("mich.primitive", code.prim, annots, argsML)
    @staticmethod
    def hashString(s):
        return hashed(window.smartmlCtx.call("hashString", s))

class Contract:
    def __init__(self, **kargs):
        self.init(**kargs)
    def setup(self):
        self.currentBlock = None
        self.hasSetup = True
        self.exp = self.export
    def init(self, **kargs):
        if not hasattr(self, 'hasSetup'):
            self.setup()
        if not hasattr(self, 'verbose'):
            self.verbose = False
        if not hasattr(self, 'messages'):
            self.messages = {}
        if not hasattr(self, 'execMessageClass'):
            self.execMessageClass = ""
        if not hasattr(self, 'title'):
            self.title = ""
        if 'data' in kargs:
            self.storage = kargs['data']
        else:
            self.storage = record(**kargs)
        self.collectMessages()
        sp.types.unknownIds = 0
    def addMessage(self, addedMessage):
        sp.profile("addMessage begin " + addedMessage.name)
        addedMessage.contract = self
        mb = MessageBuilder(addedMessage)
        self.mb = mb
        sp.setMB(mb)
        addedMessage.f(self, Expr("params", []))
        self.mb = None
        sp.setMB(None)
        self.messages[addedMessage.name] = mb
        setattr(self, addedMessage.name, addedMessage)
        sp.profile("addMessage end " + addedMessage.name)
    def buildExtraMessages(self):
        pass
    def collectMessages(self):
        sp.profile("CollectMessages begin " + self.__class__.__name__)
        self.data = sp.getData()
        for f in dir(self):
            attr = getattr(self, f)
            if isinstance(attr, AddedMessage):
                self.addMessage(AddedMessage(attr.name, attr.f))
        self.buildExtraMessages()
        #self.smartml = window.buildSmartlmJS(self)
        self.smartml = Smartml(self)
        sp.profile("CollectMessages smartml " + self.__class__.__name__)
        self.data = self.getData()
        if window.activeScenario is not None:
            self.data = Expr("contractData", [self.smartml.contractId])
        sp.profile("CollectMessages end " + self.__class__.__name__)
    def export(self):
        result = "(storage %s\nmessages (%s))" % (self.storage.export(),
                                                    (" ".join("(%s %s)" % (k, v.export()) for (k, v) in sorted(self.messages.items()))))
        if self.verbose:
            alert("Creating\n\n%s" % result)
            window.console.log(result)
        return result
    def pp(self):
        return "data:\n  %s\nmethods:\n  %s" % ("\n  ".join("%-15s = %s" % (k, spExpr(v).pp()) for (k, v) in self.initVariables.items()),
                                                "\n  ".join("\n  @message\n  def %s(self, ctt):\n%s" % (k, v.pp()) for (k, v) in self.messages.items()))
    def html(self):
        return self.smartml.html()
    def fullHtml(self):
        sp.profile("fullHtml begin " + self.__class__.__name__)
        result = self.smartml.fullHtml()
        sp.profile("fullHtml end " + self.__class__.__name__)
        return result
    def simulation(self, linenb):
        sp.profile("simulationHtml begin " + self.__class__.__name__)
        result = self.smartml.simulation(linenb)
        sp.profile("simulationHtml end " + self.__class__.__name__)
        return result
    def getStorageType(self):
        return self.smartml.getStorageType()
    def getStorageValue(self):
        return self.smartml.getStorageValue()
    def getData(self):
        return self.smartml.getStorageValue()
    def setNow(self, time):
        return self.smartml.setNow(time)
    def smartpy(self):
        return self.smartml.smartpy()
    def __repr__(self):
        return str(self.smartml)

class AddedMessage:
    def __init__(self, name, f):
        self.name = name
        self.f    = f
    def __call__(self, params = None, **kargs):
        return ExecMessage(self.contract, self.name, params, kargs)

def entryPoint(f, name = None):
    if name is None:
        name = f.__name__
    return AddedMessage(name, f)

self    = Expr("self", [])
sender  = Expr("sender", [])
source  = Expr("source", [])
amount  = Expr("amount", [])
balance = Expr("balance", [])
now     = Expr("now", [])

def append(t, x):
    return sp.append(t, x)

defaultVerifyMessage = None
def verify(cond, ghost = False, message = None):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    sp.setLineNumber(lineno)
    if message is None:
        message = defaultVerifyMessage
    if message is None:
        return sp.newCommand(Expr("verify", [spExpr(cond), ghost]))
    else:
        return sp.newCommand(Expr("verify", [spExpr(cond), ghost, spExpr(message)]))
def ghostCheck(cond):
    return check(cond, True)

## Control
def elseBlock():
    b = CommandBlock(sp)
    sp.newCommand(Expr("elseBlock", [b]))
    return b
def whileBlock(condition):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    b = CommandBlock(sp)
    sp.newCommand(Expr("whileBlock", [spExpr(condition), b, lineno]))
    return b
def if_some(condition, name):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    b = CommandBlock(sp)
    sp.newCommand(Expr("ifSomeBlock", [spExpr(condition), name, b, lineno]))
    value = Expr("openVariant", [spExpr(condition), "Some"])
    value.__asBlock = b
    b.value = value
    return value
def ifVariantBlock(value):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    b = CommandBlock(sp)
    sp.newCommand(Expr("ifVariantBlock", [spExpr(value), b, lineno]))
    return b
def ifBlock(condition):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    b = CommandBlock(sp)
    sp.newCommand(Expr("ifBlock", [spExpr(condition), b, lineno]))
    return b
def forBlock(name, value):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    value = spExpr(value)
    b = CommandBlock(sp)
    t = sp.types.unknown("for %s" % name)
    sp.newCommand(Expr("forGroup", [name, t, value, b, lineno]))
    value = Expr("iter", [name, t])
    value.__asBlock = b
    b.value = value
    return value
def updateMap(map, key, value):
    return Expr("updateMap", [spExpr(map), spExpr(key), spExpr(value)])
def ediv(num, den):
    return Expr("ediv", [spExpr(num), spExpr(den)])
def pack(value):
    return Expr("pack", [spExpr(value)])
def blake2b(value):
    return Expr("hashCrypto", ["BLAKE2B", spExpr(value)])
def sha512(value):
    return Expr("hashCrypto", ["SHA512", spExpr(value)])
def sha256(value):
    return Expr("hashCrypto", ["SHA256", spExpr(value)])
def range(a, b, step = 1):
    return Expr("range", [spExpr(a), spExpr(b), spExpr(step)])
def sum(value):
    return Expr("sum", [value])
def checkSignature(pk, sig, msg):
    return Expr("checkSignature", [pk, sig, msg])
def sign(e):
    return Expr("sign", [e])
def spmax(x, y):
    return Expr("max", [spExpr(x), spExpr(y)])
def spmin(x, y):
    return Expr("min", [spExpr(x), spExpr(y)])
def splitTokens(m, quantity, totalQuantity):
    return (Expr("splitTokens", [spExpr(m), spExpr(quantity), spExpr(totalQuantity)]))
def expr(v):
    return spExpr(v)

def nat(v):
    return Expr("nat", [spExpr(v)])
def setInt(v):
    return Expr("int", [spExpr(v)])
def toInt(v):
    return Expr("toInt", [spExpr(v)])
def isNat(v):
    return Expr("isNat", [spExpr(v)])
def asNat(v):
    return isNat(v).openSome()

def newLocal(name, value, t = "UNKNOWN"):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    sp.setLineNumber(lineno)
    return sp.newLocal(name, value, t)
def transfer(arg, amount, destination):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    sp.setLineNumber(lineno)
    sp.newCommand(Expr("transfer", [spExpr(arg), spExpr(amount), spExpr(destination)]))
def contract(argType, address):
    argType = sp.types.conv(argType)
    return Expr("contract", [sp.types.conv(argType), spExpr(address)])
def setType(var, t):
    if not window.inBrowser:
        lineno = -1
    else:
        lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
    sp.setLineNumber(lineno)
    result = Expr("setType", [spExpr(var), sp.types.conv(t)])
    sp.newCommand(result)
    return result
def type_of(e):
    return Expr("type_of", [e])
def profile(s):
    sp.profile(s)
def setProfiling(b):
    sp.profiling     = b
    sp.profilingLogs = []

def fst(e):
    return Expr("first", [spExpr(e)])
def snd(e):
    return Expr("second", [spExpr(e)])

types = sp.types

normalMax = max
smartpyio.mymax = spmax
max = spmax
min = spmin

class Scenario:
    def __init__(self):
        self.messages = []
        self.smartml = Smartml(None)
        self.exceptions = []
    def acc(self, message, show):
        if isinstance(message, str):
            if show:
                self.messages.append(message)
        else:
            self.messages += [self.setShow(x, show) for x in message]
    def setShow(self, x, show):
        x['show'] = show
        return x
    def register(self, element, show = False):
        if isinstance(element, Contract):
            self.acc(element.fullHtml(), show)
        else:
            self.acc(element.html(), show)
    def __iadd__(self, element):
        self.register(element, True)
        return self
    def add(self, *elements):
        for element in elements:
            self.register(element, True)
        return self
    def pp(self):
        if window.inBrowser:
            return '\n'.join(self.messages)
        else:
            return self.messages
    def allContracts(self):
        result = self.smartml.emptyContractMap();
        for contract in window.contracts.values():
            self.smartml.addContract(contract.contractId, contract.contract, result);
        return result
    def verify(self, condition):
        if isinstance(condition, pyBool):
            if not condition:
                raise Exception("Assert Failure")
        else:
            if window.inBrowser:
                expr = self.smartml.importExpr(condition)
                contracts = self.allContracts()
                value = self.smartml.evalExprWithContracts(expr)
                if not self.smartml.ctx.call('bool_of_value', value):
                    expr = self.smartml.string_of_expr(expr)
                    self.messages.append("<br><span class='partialType'>Assert Failure: %s</span>" % expr)
                    self.exceptions.append(Exception("Assert Failure: %s" % expr))
            else:
                data = {}
                data['action']    = 'verify'
                data['condition'] = condition.export()
                self.messages += [data]
    def compute(self, expression):
        if window.inBrowser:
            expr = self.smartml.importExpr(expression)
            contracts = self.allContracts()
            value = self.smartml.evalExprWithContracts(expr)
            self.messages.append("<span >Compute: %s == %s</span>" % (self.smartml.string_of_expr(expr), self.smartml.string_of_value(value)))
        else:
            data = {}
            data['action']     = 'compute'
            data['expression'] = expression.export()
            self.messages += [data]

    def p(self, s):
        return self.tag("p", s)
    def h1(self, s):
        return self.tag("h1", s)
    def h2(self, s):
        return self.tag("h2", s)
    def h3(self, s):
        return self.tag("h3", s)
    def h4(self, s):
        return self.tag("h4", s)
    def tag(self, tag, s):
        if window.inBrowser:
            self.messages.append("<%s>%s</%s>" % (tag, s, tag))
        else:
            data = {}
            data['action'] = 'html'
            data['tag']    = tag
            data['inner']  = s
            self.messages += [data]
    def simulation(self, c):
        if window.inBrowser:
            lineno = pyInt(getattr(getattr(inspect.currentframe(), "$stack")[-3][1], '$line_info').split(',')[0])
            return self.p(c.simulation(lineno))
        else:
            self.p("No interactive simulation available outofbrowser.")

def testScenario():
    scenario = Scenario()
    window.activeScenario = scenario
    return scenario

def send(destination, amount):
    transfer(unit, amount, contract(TUnit, destination).openSome())

testTrace = testScenario

# For backward "compatibility"
def Record(**args):
   raise Exception("sp.Record is obsolete, please use sp.record.")
def BigMap(**args):
   raise Exception("sp.BigMap is obsolete, please use sp.bigMap.")
def Map(**args):
   raise Exception("sp.Map is obsolete, please use sp.map.")
def Set(**args):
   raise Exception("sp.Set is obsolete, please use sp.set.")


# Library

def vector(xs, tkey = TIntOrNat, tvalue = "UNKNOWN"):
    return map(l = {k : v for (k, v) in enumerate(xs)}, tkey = tkey, tvalue = tvalue)

def matrix(xs, tkey = TIntOrNat, tvalue = "UNKNOWN"):
    return vector([vector(x, tkey = tkey, tvalue = tvalue) for x in xs], tkey = tkey)

def cube(xs, tkey = TIntOrNat, tvalue = "UNKNOWN"):
    return vector([matrix(x, tkey = tkey, tvalue = tvalue) for x in xs], tkey = tkey)
