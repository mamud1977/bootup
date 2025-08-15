import pytest

from app.py_package.subpkg3.subpkg3 import fn_subpkg3

def test_fn_subpkg3():
   assert fn_subpkg3('{"name": "Mamud", "age": 40}') == True

