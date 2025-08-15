from py_package import mainpkg1
from py_package import mainpkg2
from py_package.subpkg2 import subpkg2
from py_package.subpkg3.subpkg3 import fn_subpkg3
    
mainpkg1.fn_mainpkg()
mainpkg2.fn_mainpkg()
subpkg2.fn_subpkg2()


ret = fn_subpkg3('{"name": "Abrar"}')