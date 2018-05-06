#!python
import os
import subprocess


def unitTestAction(target, source, env):
    '''
    Action for a 'UnitTest' builder object.
    Runs the supplied executable, reporting failure to scons via the test exit status.
    When the test succeeds, the file target.passed is created to indicate that
    the test was successful and doesn't need running again unless dependencies change.
    '''
    app = str(source[0].abspath)
    if subprocess.call(app) == 0:
        open(str(target[0]), 'w').write("PASSED\n")
    else:
        return 1


def unitTestActionString(target, source, env):
    '''
    Return output string which will be seen when running unit tests.
    '''
    return 'Running tests in ' + str(source[0])


def ConvertStrToList(source):
    if isinstance(source, str):
        source = [source]
    return source


def addUnitTest(env, target=[], source=[], *args, **kwargs):
    '''
    Add a unit test
    Parameters:
        target - If the target parameter is present, it is the name of the test executable.
            The default target is 'bin/testName', where 'testName' is the first element in the source.
        source - list of source files to create the test executable.
        any additional parameters are passed along directly to env.Program().
    Returns:
        The scons node for the unit test.

    Any additional files listed in the env['UTEST_MAIN_SRC'] build variable are
    also included in the source list.

    All tests added with addUnitTest can be build with the test alias:
        "scons test"
    Any test can be build in isolation from other tests, using the name of the
    test executable provided in the target parameter:
        "scons target"

    All tests added with addUnitTest can be run with the argument:
        "scons test=all"
    Any test can be built in isolation from other tests, using the name of the
    test executable, or part of this name, provided in the target parameter:
        "scons test=target"
    '''
    # If unit testing is off
    if env['test'] == ['off']:
        return None

    # Convert string to list
    target = ConvertStrToList(target)
    source = ConvertStrToList(source)

    # If user does not give any parameter
    if not target and not source:
        return None

    # If user gives only a target
    if not source:
        source = target
        target = []

    source_name = os.path.basename(source[0])  # test.cpp
    source_basic_name = os.path.splitext(source_name)  # test

    # Set default target
    if not target:
        target = ['#bin/' + source_basic_name[0] + '.out']

    # source.append(env['UNIT_TEST_MAIN_SRC'])
    source.insert(0, env['UNIT_TEST_MAIN_SRC'])
    program = env.Program(target, source, *args, **kwargs)

    unit_test = env.UnitTest(program)
    # Run the test when test=all
    if env['test'] == ['all']:
        env.AlwaysBuild(unit_test)
    # Run the test if env['test'] contain a part of the test name
    else:
        for test in env['test']:
            if test.lower() in source_basic_name[0].lower():
                env.AlwaysBuild(unit_test)

    # add alias to build all unit tests.
    env.Alias('test', unit_test)
    # make an alias to build the test in isolation from the rest of the tests.
    env.Alias(source_basic_name[0], unit_test)
    return unit_test


# -------------------------------------------------------------------------------
# Functions used to initialize the unit test tool.
def generate(env, unit_test_main_src=None, libs=None):
    if unit_test_main_src is None:
        unit_test_main_src = []
    if libs is None:
        libs = []

    env['BUILDERS']['UnitTest'] = env.Builder(
        action=env.Action(unitTestAction, unitTestActionString),
        suffix='.passed')
    env['UNIT_TEST_MAIN_SRC'] = unit_test_main_src
    env.AppendUnique(LIBS=libs)
    # Add a Method for the UnitTest builder
    env.AddMethod(addUnitTest, "addUnitTest")


def exists(env):
    return 1
