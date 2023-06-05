import glob
from os.path import basename, dirname, isfile
from Miku import MOD_LOAD, LOG,MOD_NOLOAD


def __list_all_modules():        
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith('__init__.py')
    ]

    if MOD_LOAD or MOD_NOLOAD:
        to_load = MOD_LOAD
        if to_load:
            if not all(
                    any(mod == module_name
                        for module_name in all_modules)
                    for mod in to_load):
                LOG.print("Invalid Loaders Exiting...")
                quit(1)

            all_modules = sorted(set(all_modules) - set(to_load))
            to_load = list(all_modules) + to_load

        else:
            to_load = all_modules

        if MOD_NOLOAD:
            LOG.print(f"Not Loading :- {MOD_NOLOAD}")
            return [item for item in to_load if item not in MOD_NOLOAD]

        return to_load

    return all_modules


ALL_MODULES = __list_all_modules()
LOG.print(f"Modules To Load :-  {str(ALL_MODULES)}")
__all__ = ALL_MODULES + ["ALL_MODULES"]
