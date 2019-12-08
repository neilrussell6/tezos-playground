## Copyright 2019 Smart Chain Arena LLC. ##

import traceback

from vendor.SmartPyBasic.browser import alert, window

window.activeScenario = None
window.contracts = {}

class Test:
    def __init__(self, name, shortname, f, profile):
        self.name      = name
        self.shortname = shortname
        self.profile   = profile
        self.f         = f

    def eval(self):
        import vendor.SmartPyBasic.smartpy as smartpy
        smartpy.setProfiling(self.profile)
        smartpy.profile("start")
        window.activeScenario = None
        window.contractNextId = 0
        window.contracts = {}
        window.validityErrors = []
        try:
            self.f()
        finally:
            if window.activeScenario is not None:
                window.setOutput(window.activeScenario.pp())
                for e in window.activeScenario.exceptions:
                    raise e
            if window.validityErrors:
                badValidityText = "Bad validity for some transactions %s\nPlease use c.entryPoint.run(valid = ..expected validation..)" % (' '.join(" <button class=\"text-button\" onClick='showLine(%s)'>(line %s)</button>" % (lineId, lineId) for lineId in window.validityErrors))
                raise Exception(badValidityText)
        smartpy.profile("end")
        if self.profile:
            addOutput("<hr/><h4>Profiling</h4>" + "<br>".join(smartpy.sp.profilingLogs))

window.pythonTests = []
def addTest(name, shortname = None, profile = False):
    if shortname is None:
        shortname = name
    if any(x.shortname == shortname for x in window.pythonTests):
        raise Exception("Already defined test %s" % shortname)
    for x in shortname:
        if not (x in "_-" or x.isalnum()):
            raise Exception("Bad test name: '%s', '%s' is forbidden\nTo solve the issue, you can add a shortname by doing, e.g.,\n\naddTest(name = '%s', shortname='%s')" % (shortname, x, name, ''.join(x for x in shortname if x in "_-" or x.isalnum())))
    def r(f):
        window.pythonTests.append(Test(name, shortname, f, profile))
    return r


def setOutput(s):
    window.setOutput(s)
def addOutput(s):
    window.addOutput(s)
def tag(t, s):
    return "<%s>%s</%s>" % (t, s, t)
def p(s):
    return tag("p", s)
def h1(s):
    return tag("h1", s)
def h2(s):
    return tag("h2", s)
def h3(s):
    return tag("h3", s)
def h4(s):
    return tag("h4", s)

context = globals().copy()
context['alert'] = alert
context['window'] = window
reverseLines = {}


def formatErrorLine(line):
    i = -1
    while i+2 < len(line) and line[i + 1] == ' ':
        i += 1
    if 0 <= i:
        line = i * "&nbsp;" + line[i + 1:]
    return line

def showTraceback(title, trace):
    title="Error: " + str(title)
    lines = []
    skip = False
    for line in trace.split('\n'):
        if not line:
            continue
        if skip:
            skip = False
            continue
        skip = 'module __main__' in line and False
        if not skip:
            lineStrip = line.strip()
            lineId = None
            line = formatErrorLine(line)
            if lineStrip.startswith('module <module>') or lineStrip.startswith('File <string>'):
                lineId = line.strip().split()[3].strip(',')
                line = line.replace(lineId, reverseLines.get(lineId, lineId))
            line = line.replace('module <module>', 'SmartPy code').replace('File <string>', 'SmartPy code')
            if 'SmartPy code' in line:
                line = "<span class='partialType'>%s</span>" % (line)
            if lineId:
                line = line + " <button class=\"text-button\" onClick='showLine(%s)'>(line %s)</button>" % (lineId, lineId)
            lines.append(line)
    error = title + '\n\n' + lines[0] + '\n\n' + '\n'.join(lines[1:-1])
    window.showError("<div class='michelson'>%s</div>" % (error.replace('\n', '\n<br>')))

def evalTest(name):
    for test in window.pythonTests:
        if test.name == name:
            test.eval()

def adaptBlocks(code):
    lines = code.split('\n') + ['']
    def indent(line):
        result = 0
        for i in line:
            if i == ' ':
                result += 1
            else:
                break
        return result
    blocks = []
    lineId = 0
    newLines = []
    class NewLine:
        def __init__(self, pos, line):
            if pos is None:
                pos = -1
            self.pos = pos
            self.line = line
    for line in lines:
        initialLine = line
        lineId += 1
        newIndent = indent(line)
        stripped = line.strip()
        nline = line.strip(' \r')
        if line[newIndent:].startswith('sp.for '):
            p = nline[:-1].split(' ')
            if nline[-1] == ':' and p[0] == 'sp.for' and p[2] == 'in':
                line = "%swith sp.forBlock('%s', %s) as %s:" % (newIndent * ' ', p[1], ' '.join(p[3:]), p[1])
        elif line[newIndent:].startswith('sp.if '):
            p = nline[:-1].split(' ')
            if nline[-1] == ':' and p[0] == 'sp.if':
                line = "%swith sp.ifBlock(%s):" % (newIndent * ' ', ' '.join(p[1:]))
        elif line[newIndent:].startswith('sp.while '):
            p = nline[:-1].split(' ')
            if nline[-1] == ':' and p[0] == 'sp.while':
                line = "%swith sp.whileBlock(%s):" % (newIndent * ' ', ' '.join(p[1:]))
        elif line[newIndent:].startswith('sp.else ') or line[newIndent:].startswith('sp.else:'):
            if nline[-1] == ':':
                line = "%swith sp.elseBlock():" % (newIndent * ' ')
        if initialLine.endswith('\r') and not line.endswith('\r'):
            line += '\r'
        newLines.append(NewLine(lineId, line))
    result = '\n'.join(line.line for line in newLines)
    global reverseLines
    reverseLines.clear()
    for i in range(len(newLines)):
        reverseLines[str(i + 1)] = str(newLines[i].pos)
    return result

testTemplate="""
@addTest(name = "%s test")
def test():
    # define a contract
    c1 = %s(..)
    scenario  = sp.testScenario()
    # scenario += c1.myEntryPoint(..)
    # scenario += c1.myEntryPoint(..)
    # scenario += c1.myEntryPoint(..)
    # scenario.verify(..)
"""

def run(withTests):
    window.pythonTests.clear()
    window.cleanAll()
    import smartpy
    smartpy.defaultVerifyMessage=None
    code = window.editor.getValue()
    code = adaptBlocks(code)
    env = context.copy()
    exec(code, env)
    window.cleanAll()
    for test in window.pythonTests:
        window.addButton(test.name, test.f)
        if withTests:
            test.eval()
    if withTests and len(window.pythonTests) == 0:
        html = ""
        for c in env:
            if '$' in c:
                continue
            if hasattr(env[c], 'collectMessages'):
                html += "<span class='partialType'>Warning:</span> There is a sp.Contract class '%s' but no test is defined.<br><br>Please add a test such as:<br><br><pre>%s</pre>" % (str(c), testTemplate % (c, c))
        if html:
            setOutput(html)

def parseMicheline(address, res):
    #window.console.log(res);
    balance   = res['balance']
    #counter   = res['counter']
    #delegate  = res['delegate']
    if 'manager' in res:
        manager   = res['manager']
    else:
        manager = ''
    try:
        script = res['script']
    except:
        script = None
    import smartpy
    smartml = smartpy.Smartml(None)
    if script:
        code     = script['code']
        storage  = script['storage']
        for c in code:
            if c.prim == 'storage':
                typeStorage = smartml.parseMich(c.args[0])
            if c.prim == 'parameter':
                typeParameter = smartml.parseMich(c.args[0])
            if c.prim == 'code':
                innerCode = smartml.parseMich(c.args[0])
        code     = smartml.parseMich(code)
        storage = smartml.parseMich(storage)
        #fullCode = "storage{\n%s\n}\n\ncode{\n%s\n}" % (smartml.ppMichStorage(storage, "  "), smartml.ppMich(code, "  "))
        # example: KT1Q1kfbvzteafLvnGz92DGvkdypXfTGfEA3
    else:
        #fullCode = "No code available for this contract."
        typeStorage = None
        typeParameter = None
        storage = None
        # example: KT1F1EfPahaN35gi6aCYB93xV5W6HgVEiZuQ
    smartml.ppMichInfos(address, str(balance), str(manager))
    if typeStorage:
        smartml.ppMessageBuilder(storage, typeStorage, typeParameter, innerCode)

def onContract(address, cont):
    window.onContract(address, cont)

def showCommands(platform):
    l = []
    commands = window.editor.commands.commands
    for c in sorted(commands):
        try:
            l.append("%-40s : %s" % (c, commands[c].bindKey[platform]))
        except:
            pass
    return "<pre>%s</pre>" % '\n'.join(l)

def toException(x):
    return Exception(x)

def ppMichelson(code, withComments):
    lines = [x.strip() for x in code.split('\n')]
    def split(s):
        if '#' in s:
            pos = s.index('#')
            return s[:pos].strip(), s[pos:].strip()
        return s.strip(), None
    lines = [split(x) for x in lines if x]
    result = []
    for s, c in lines:
        if not withComments:
            c = None
        s = s.replace('{', ' { ').replace('}', ' } ').replace('(', ' ( ').replace(')', ' ) ').replace(" ;", ";").replace(" ;", ";").strip()
        split = s.split()
        cursor = 0
        if s == "" and c:
            result.append((s, c))
        while len(split):
            if split[cursor] in ["parameter", "storage", "code"]:
                result.append((' '.join(split[0:cursor + 1]), None))
                split = split[cursor + 1:]
                continue
            if split[cursor] in ["{", "}", "};", ";"]:
                if cursor != 0:
                    result.append((' '.join(split[0:cursor]), None))
                    split = split[cursor:]
                    cursor = 0
                else:
                    result.append((' '.join(split[0:cursor + 1]), None))
                    split = split[cursor + 1:]
            elif len(split) == cursor + 1:
                result.append((' '.join(split[0:cursor + 1]), c))
                split = []
            elif split[cursor].endswith(';'):
                result.append((' '.join(split[0:cursor + 1]), None))
                split = split[cursor + 1:]
                cursor = 0
            else:
                cursor += 1
    lines     = result
    parameter = []
    storage   = []
    code      = []
    init      = []
    result = {'init': init, 'parameter': parameter, 'storage': storage, 'code': code}
    step      = 'init'
    indent    = ""
    for (s, c) in lines:
        if s == '{':
            indent = indent + "  "
            nextIndent = indent + "  "
        elif '}' in s:
            indent = indent [:-2]
            nextIndent = indent [:-2]
        else:
            nextIndent = indent
        if s in ["parameter", "storage", "code"]:
            step = s
        line = (indent + ("%-10s %s" % (s, c) if c else s)) if step != "init" else (("%s %s" % (s, c)).strip() if c else s)
        if line:
            result[step].append(line)
        indent = nextIndent
    if init:
        init = '\n'.join(init) + '\n\n'
    else:
        init = ""
    michelson = "%s%s\n\n%s\n\n%s" % (init,
                                  ' '.join(parameter).replace(' )', ')').replace('( ', '(').replace(' ;', ';'),
                                  ' '.join(storage)  .replace(' )', ')').replace('( ', '(').replace(' ;', ';'),
                                  '\n'.join(code))
    return michelson

def ppMichelsonEditor(withComments):
    return ppMichelson(window.editor.getValue(), withComments)

def ppMichelsonEditorCompress():
    return removeCommentsMichelson(ppMichelson(window.editor.getValue(), False))

def compressMichelson(lines):
    result = []
    inSeq = False
    for line in lines:
        row = line.split()
        seqOK = "{" not in line and "}" not in line and row[-1][-1] == ';' and not row[0].startswith('parameter') and not row[0].startswith('storage')
        if inSeq and seqOK:
            result[-1] += " " + ' '.join(row)
        else:
            result.append(line)
            inSeq = seqOK
    return result

def removeCommentsMichelson(michelson):
    lines = [x[:x.index('#')].rstrip() if '#' in x else x for x in michelson.split('\n')]
    lines = [x for x in lines if x.strip()]
    lines = compressMichelson(lines)
    return '\n'.join(lines)

window.evalTest                  = evalTest
window.evalRun                   = run
window.showTraceback             = showTraceback
window.parseMicheline            = parseMicheline
window.showCommands              = showCommands
window.toException               = toException
window.ppMichelsonEditor         = ppMichelsonEditor
window.ppMichelsonEditorCompress = ppMichelsonEditorCompress
window.removeCommentsMichelson   = removeCommentsMichelson
window.cleanOutputPanel()
