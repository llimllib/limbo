# -*- coding: UTF-8 -*-
import os
import subprocess
import shlex

from nose.tools import eq_

DIR = os.path.dirname(os.path.realpath(__file__))
TESTPLUGINS = os.path.join(DIR, "plugins")

# http://stackoverflow.com/a/13160748/42559
def sh(cmd):
     proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
     output = proc.communicate()[0].decode("utf8")
     ret = proc.returncode
     return output, ret

def test_cmd():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    out, ret = sh(u"limbo -c '{0}' --pluginpath {1}".format(msg, TESTPLUGINS).encode("utf8"))
    out = out.strip()
    eq_(out, msg)
    eq_(ret, 0)

def test_repl():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    proc = subprocess.Popen(["limbo", "-t", "--pluginpath", TESTPLUGINS], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    out = proc.communicate(msg.encode("utf8"))[0]
    out = out.strip().decode("utf8")
    eq_(out, u"limbo> {0}\nlimbo>".format(msg))
    ret = proc.returncode
    eq_(ret, 0)

# XXX: TODO
#def test_hook():
#    out, ret = sh(u"limbo -c '' --pluginpath {0} --hook loop".format(TESTPLUGINS))
#    out = out.strip()
#    eq(out, ["init"])
