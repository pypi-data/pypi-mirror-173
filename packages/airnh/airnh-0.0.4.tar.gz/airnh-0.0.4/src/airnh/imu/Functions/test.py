import importlib.util as iu

def imp_mod(name):
    spec = iu.find_spec(name)
    mod = iu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

mod = imp_mod("TestCases.testbase")    
print(mod.compNum(1,1))
