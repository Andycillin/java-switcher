'''
MIT License
Copyright (c) 2019 Thien Phuc Tran
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import subprocess
import plistlib
from os.path import expanduser
import os
import sys

LINE_MARKER = '### java-switcher'

def get_java_versions():
    process = subprocess.Popen(['/usr/libexec/java_home', '-X'], stdout=subprocess.PIPE)
    out, err = process.communicate()

    return plistlib.readPlistFromString(out)

def print_available_versions(plist):
    headers = ['Choice', 'Java Version', 'JAVA_HOME']
    fstr = '{0:>10s}\t{1:10s}\t{2:10s}'

    print fstr.format(*headers)
    for idx, ver in enumerate(plist):
        print fstr.format(str(idx + 1), ver['JVMName'], ver['JVMHomePath'])

def get_bash_profile_path():
    return expanduser('~/.bash_profile')


def overwrite_java_home(java_home):
    if os.path.isfile(get_bash_profile_path()):
        with open(get_bash_profile_path(), 'r') as f:
            content = f.read().splitlines()
    else:
        content = []

    template = 'export JAVA_HOME={} ' + LINE_MARKER + '\n'
    lines = [(l + '\n') for l in content if not l.endswith(LINE_MARKER)]
    lines.append(template.format(java_home))

    with open(get_bash_profile_path(), 'w') as f:
        f.writelines(lines)

def switch_to_jv(jv):
    java_home = jv['JVMHomePath']
    overwrite_java_home(java_home)
    print 'Switched to {}.\nClose terminal and open again for it to take effect.'.format(jv['JVMName'])

def select_version_cmdline(version, plist):
    for ver in plist:
        if ver['JVMVersion'].startswith(version):
            switch_to_jv(ver)
            return

    print 'No matching Java version: ' + version

def main():
    plist = get_java_versions()
    print_available_versions(plist)

    valid = False
    while not valid:
        try:
            choice = raw_input("Enter choice: ")
            choice = int(choice)
            if 0 < choice <= len(plist):
                switch_to_jv(plist[choice - 1])
                valid = True
            else:
                raise ValueError
        except ValueError:
            print ('Invalid choice')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        select_version_cmdline(sys.argv[1], get_java_versions())
