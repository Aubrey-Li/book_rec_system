# a function for simulating tests. The first argument
# is a string with a descriptive name. The second and
# third arguments are the test and answer expressions
def test(descr, v1, v2):
  if not(v1 == v2):
    print("The following values were expected to be equal, but weren't:")
    print(v1)
    print(v2)
    print()
    raise Exception("Tests failed")
  else:
    print(descr + " passed")

# v_func needs to be a function that takes no arguments and
# runs the expression you want to test
def testValueError(descr, v_func):
  try:
    v_func()
    print(descr + " failed (did not raise an error)")
  except ValueError:
    print(descr + " passed (raised error as expected)")

'''
# A simple function that raises an error when given 5 as input --
# this is just here to show how to write tests that raise errors
def error_five(x : int):
  if x == 5:
    raise ValueError("got 5")
  else:
    return x

# a test that should raise an error
testValueError("try 5", lambda: error_five(5))

# a test that will not raise an error, so the report will show the test failed
testValueError("try 4", lambda: error_five(4))

# if a test should not raise an error, use the existing test function
test("try 4 expect to run", 4, 4)
'''
