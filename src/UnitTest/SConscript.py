#!python

Import('testEnv')

# Load and Compile main class for test - Catch2
objTestMain = testEnv.Object('Catch2Main.cpp')

# Add new tool, that can be found in UnitTest.py
testEnv.Tool('UnitTest',
             toolpath=['.'],
             unit_test_main_src=objTestMain[0].abspath)
