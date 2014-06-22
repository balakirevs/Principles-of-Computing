"""
Lightweight testing class inspired by unittest from Pyunit
https://docs.python.org/2/library/unittest.html
Note that code is designed to be much simpler than unittest
and does NOT replicate uinittest functionality
"""


class TestSuite:
    """
    Create a suite of tests similar to unittest
    """

    def __init__(self):
        """
        Creates a test suite object
        """
        self.total_tests = 0
        self.failures = 0

    def run_test(self, computed, expected, message = ""):
        """
        Compare computed and expected expressions as strings
        If not equal, print message, computed, expected
        """
        self.total_tests += 1
        if computed != expected:
            print message + " failed." + " Computed: " + str(computed) + \
                  " Expected: " + str(expected)
            self.failures += 1
        else:
            print message + " succeeded." + " Computed: " + str(computed) + \
                  " Expected: " + str(expected)

    def report_results(self):
        """"
        Report back summary of successes and failures
        from run_test()
        """
        print "Ran " + str(self.total_tests) + " tests. " \
              + str(self.failures) + " failures."
