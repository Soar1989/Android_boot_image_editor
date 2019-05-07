#!/usr/bin/env python3
import sys, subprocess, re

def parseClassName(inFileName):
    out = subprocess.check_output("javap %s" % inFileName, shell = True).decode("utf-8").split("\n")
    className = None
    for line in out:
        matched = re.match("public.*class\s+(.*)\s+{", line)
        if matched:
            className = matched.group(1)
    return className

def parseClassPath(inFileName):
    print(inFileName)
    aClassName = parseClassName(inFileName)
    if aClassName:
        qName = aClassName.replace(".", "/") + ".class"
        return inFileName[:inFileName.index(qName)], aClassName
    else:
        raise

def genJNI(inFileName):
    parsedClassPath, parsedClassName = parseClassPath(inFileName)
    cmd = "javah -jni -v -d out -cp %s %s" % (parsedClassPath, parsedClassName)
    print(cmd)
    output = subprocess.check_output(cmd, shell = True).decode()
    print(output.strip())

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise
    else:
        genJNI(sys.argv[1])
else:
    print("DO NOTHING")
