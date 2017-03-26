import os
import unittest

# Initialize the test suite
loader = unittest.TestLoader()
suite = loader.discover(os.path.dirname(__file__), '*Test.py')

# Initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
