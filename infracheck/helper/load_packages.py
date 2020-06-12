import inspect
import logging
import os
import pkgutil
from typing import Any

log = logging.getLogger("pck_loader")


def load_packages(package, class_object: Any):
    """
    Recursively walk the supplied package to retrieve all packages that inherit from class_object
    """
    packages = []
    seen_paths = []
    imported_package = __import__(package, fromlist=['blah'])
    for _, plugin_name, is_package in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
        if not is_package:
            plugin_module = __import__(plugin_name, fromlist=['blah'])
            class_members = inspect.getmembers(plugin_module, inspect.isclass)
            for (_, c) in class_members:
                # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                if issubclass(c, class_object) & (c is not class_object):
                    if 'modules' not in str(c.__module__):
                        log.info(f'\nPlugin: {c.__name__}')
                    else:
                        log.info(f'|-- {c.__name__}')
                    packages.append(c())

    # Now that we have looked at all the modules in the current package, start looking
    # recursively for additional modules in sub packages
    all_current_paths = []
    if isinstance(imported_package.__path__, str):
        all_current_paths.append(imported_package.__path__)
    else:
        all_current_paths.extend([x for x in imported_package.__path__])

    for pkg_path in all_current_paths:
        if pkg_path not in seen_paths:
            seen_paths.append(pkg_path)

            # Get all sub directory of the current package path directory
            child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

            # For each sub directory, apply the walk_package method recursively
            for child_pkg in child_pkgs:
                packages = packages + load_packages(package + '.' + child_pkg, class_object)

    return packages
