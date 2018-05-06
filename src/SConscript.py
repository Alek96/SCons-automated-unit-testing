#!python

Import('env')

# Run SConscript files
libFiles = SConscript(Split('''
    module1/SConscript.py
    module2/SConscript.py
	'''))

# Load and Compile main
objFiles = env.Object('main.cpp')

# Make new library from previous
libFiles = env.Library('ProjectLib', libFiles)

# Link program
env.Program(target='#bin/ProjectName.out', source=objFiles + libFiles)
