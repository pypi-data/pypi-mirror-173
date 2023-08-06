

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_0():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_1_0()
del _delvewheel_init_patch_1_1_0
# end delvewheel patch

import _secupy


def __getattr__(name):
    if hasattr(_secupy, name):
        return getattr(_secupy, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")
