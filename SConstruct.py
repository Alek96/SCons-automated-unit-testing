#!python
import os

env = Environment(TARGET_ARCH='x86')  # Create an environmnet for 32 bit version
# Make env global 
Export('env')

# This will be shown with flag -h
Help('''
usage: scons [OPTION] ...

SCons Options (case insensitive):
  release=1             Build the release version
  verbose=1             Build with all information

 unit test:
  test                  Build all unit tests
  testName              Build single unit test called 'testName'
  test=on               Turns on building unit tests (default)
  test=off              Turns off building unit tests
  test=all              Run all unit tests
  test=testName         Run unit tests whose name contains 'testName'

''')

# Keys to lower case (for case insensitiveness)
ARGUMENTS = dict((k.lower(), v) for (k, v) in ARGUMENTS.items())


# Generator expressions, see: https://www.python.org/dev/peps/pep-0289/


class colors:
    CYAN = '\033[36m'
    LRED = '\033[91m'
    LGREEN = '\033[92m'
    LYELLOW = '\033[93m'
    LBLUE = '\033[94m'
    LMAGENTA = '\033[95m'
    LCYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Replace long comment for short version
if ARGUMENTS.get('verbose') != '1':
    env.Append(CCCOMSTR=[colors.CYAN + 'Compiling ' + colors.ENDC + '$TARGET'])
    env.Append(CXXCOMSTR=[colors.CYAN + 'Compiling ' + colors.ENDC + '$TARGET'])
    env.Append(ARCOMSTR=[colors.LCYAN + 'Archiving ' + colors.ENDC + '$TARGET'])
    env.Append(LINKCOMSTR=[colors.LBLUE + 'Linking ' + colors.ENDC + '$TARGET'])

# Get current path
ProjectPath = [os.getcwd()]
env.Append(CPPPATH=ProjectPath)

# Set path to external library
env.SetDefault(EXTLIBPATH='')
ExtLibPath = env['EXTLIBPATH']

# Names of the external libraries.
# Letter 'd' for debug, and suffix .lib or .so will be added automatically
LibS = Split('''
	''')

# Path of the external libraries where can be found header files
ExtLibHeaders = Split('''
	''')
ExtLibHeaders = [ExtLibPath + x for x in ExtLibHeaders]
env.Append(CPPPATH=ExtLibHeaders)

# Detect the build mode
platform = ARGUMENTS.get('os', Platform())
if ARGUMENTS.get('release', '0') == '1':
    variant = 'Release'
else:
    variant = 'Debug'

# Add flags for detected platform and build mode
if platform.name == 'win32':
    if variant == 'Debug':
        env.Append(CPPDEFINES=['DEBUG', '_DEBUG'])
        env.Append(CCFLAGS=['-W3', '-EHsc', '-D_DEBUG', '/MDd', '/Z7'])
        # env.Append(CCPDBFLAGS=['/Zi', '/Fd${TARGET}.pdb'])
        env.Append(LINKFLAGS=['/DEBUG', '/INCREMENTAL:NO'])
        LibS = [x + 'd.lib' for x in LibS]
    else:
        env.Append(CPPDEFINES=['NDEBUG'])
        env.Append(CCFLAGS=['-O2', '-EHsc', '-DNDEBUG', '/MD'])
        LibS = [x + '.lib' for x in LibS]
else:  # posix and linux
    env.Append(CCFLAGS=['-std=c++14'])
    env.Append(ARFLAGS=['-T'])
    if variant == 'Debug':
        env.Append(CCFLAGS=['-g'])
        LibS = [x + 'd.so' for x in LibS]
    else:
        LibS = [x + '.so' for x in LibS]

env.Append(LIBS=LibS)
env.Append(LIBPATH=[ExtLibPath + '/lib'])

# Initial unit test
testEnv = env.Clone()
Export('testEnv')
testEnv.SConscript('src/UnitTest/SConscript.py', variant_dir='build/' + variant + '/UnitTest', duplicate=0)
# Save argument in testEnv
testEnv.SetDefault(test=[ARGUMENTS.get('test', 'on')])

# Hierarchical Builds
if not GetOption('help'):
    env.SConscript('src/SConscript.py', variant_dir='build/' + variant, duplicate=0)
