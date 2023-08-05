# AssertCount

A pytest plugin to count the actual number of asserts in a pytest run.

### Output

The output will be shown as the second last result in the pytest output, right above ````short test summary info````.<br>
Example:
```shell
...
===== assert statistics =====
total asserts : 1
passed asserts: 1 (100%)
failed asserts: 0 (0%)
== short test summary info ==
...
```

The plugin is only able to count asserts in ````test_XYZ.py```` files. When using `utils`-files name them `test_utils`.

### Setup

In order to use the plugin, you have to define a `pytest.ini` file in the root directory of your project.
This file should contain the following lines:
```shell
[pytest]
enable_assertion_pass_hook=true
```