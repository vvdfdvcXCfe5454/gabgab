import sys
from Gabbybot.config import Config


def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile

    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(f"{dirname(__file__)}/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    LOAD = getattr(Config, 'LOAD', [])
    NO_LOAD = getattr(Config, 'NO_LOAD', [])
    LOGGER = getattr(Config, 'LOGGER', True)

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(
                    any(mod == module_name for module_name in all_modules)
                    for mod in to_load
            ):
                print("[Gabby] Invalid loader names. Quitting.")
                sys.exit(1)

            all_modules = sorted(set(all_modules) - set(to_load))
            to_load = list(all_modules) + to_load
        else:
            to_load = all_modules

        if NO_LOAD:
            print(f"[Gabby] Not loading: {NO_LOAD}")
            return [item for item in to_load if item not in NO_LOAD]
        return to_load
    return all_modules


ALL_MODULES = __list_all_modules()

__all__ = ALL_MODULES + ["ALL_MODULES"]
