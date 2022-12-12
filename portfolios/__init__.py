import pkgutil
import inspect

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)

    class_obj = [x for x in inspect.getmembers(_module) if x[0] == module_name][0]
    globals()[module_name] = class_obj