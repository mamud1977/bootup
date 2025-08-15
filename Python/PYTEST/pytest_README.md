Executing all test files:
/TestAutomation$ pytest v

Executing specific file:
/TestAutomation$ pytest <filename> -v
/TestAutomation$ pytest pytest_sample1.py -v

Execute tests by substring matching
/TestAutomation$ pytest -k <substring> -v
/TestAutomation$ pytest pytest_sample1.py -k answer2 -v 
/TestAutomation$ pytest -k test_divisible_by_3 -v 


Execute tests based on markers:
/TestAutomation$ pytest -m <marker_name> -v

Creating fixtures using @pytest.fixture

conftest.py allows accessing fixtures from multiple files.

Parametrizing tests using @pytest.mark.parametrize.

Xfailing tests using @pytest.mark.xfail.
Skipping tests using @pytest.mark.skip.

Stop test execution on n failures:
/TestAutomation$ pytest -k square -v --maxfail 1

Running tests in parallel using pytest -n <num>.
/TestAutomation$ pytest -k square -v --maxfail 1 -n 2

Generating results xml using pytest -v --junitxml = "result.xml".





