# encoding: utf-8
# api: pep517
# title: flit backend
# description: wraps flit_core.buildapi
# version: 0.2
# depends: python:flit (>=3.0, <4.0)
# license: BSD-3-Clause
# priority: extra
# src: ~/.local/lib/python3.8/site-packages/flit_core/
# pylint: disable=unused-import, wrong-import-position, wrong-import-order
#
# This is supposed to become an alternative to pluginconf.setup,
# using flit as pep517 build backend. But adding automagic field
# lookup of course.
#
# It can be invoked per `flit-pluginconfig build` and requires
# a `pyproject.toml` like:
#
#       [build-system]
#       requires = ["flit_core", "pluginconf"]
#       build-backend = "pluginconf.flit"
#
#       [project]
#       name = "foobar"
#       #dynamic = ["version", "description"]
#
# Injecting attributes between ini reading and parameter collection
# turned out easier than expanding on flit_core.buildapi functions.
# And lastly, this just chains to flit.main() to handle setup and
# build steps.
#

""" monkeypatches flint to use pluginconf sources for packaging """


import sys
import re
import functools

import flit_core.common
import flit_core.config

import pluginconf
import pluginconf.setup as psetup



#-- patchy patch
def inject(where):
    """ monkeypatch into module """
    def wrapped(func):
        setattr(where, func.__name__, func)
        wrapped.__doc__ = func.__doc__
        return func
    return wrapped

@inject(flit_core.config)
def read_flit_config(path):
    """ @inject read_flit_config() with forced dynamic fields """
    ini = flit_core.config.tomli.loads(path.read_text('utf-8'))

    # make fields dynamic
    if not "dynamic" in ini["project"]:
        ini["project"]["dynamic"] = []
    for dyn in ['description', 'version']:
        if dyn in ini["project"]:
            del ini["project"][dyn]
        if not dyn in ini["project"]["dynamic"]:
            ini["project"]["dynamic"].append(dyn)
    print(ini)

    # turn it into LoadedConfig
    return flit_core.config.prep_toml_config(ini, path)

# override make_metadata
@inject(flit_core.common)
def make_metadata(module, ini_info):
    """ @inject different sourcing order to apply plugin meta fields """
    meta = {
        "name": module.name,
        "provides": [module.name]
    }
    meta.update(ini_info.metadata)
    meta.update(
        pmd_meta(
            pluginconf.plugin_meta(filename=module.file),
            ini_info
        )
    )
    if not meta.get("version"):
        meta.update(
            flit_core.common.get_info_from_module(module.file, ['version'])
        )
    return flit_core.common.Metadata(meta)

# map plugin meta to flit Metadata
def pmd_meta(pmd, ini):
    """ enjoin PMD fields with flit.common.MetaData """
    pmd = psetup.MetaUtils(pmd)
    meta = {
        "summary": pmd.description,
        "version": pmd.version,
        "home_page": pmd.url,
        "author": pmd.author,  # should split this into mail and name
        "author_email": None,
        "maintainer": None,
        "maintainer_email": None,
        "license": pmd.license,  # {name=…}
        "keywords": pmd.get_keywords(),
        "download_url": None,
        "requires_python": pmd.python_requires() or ">= 2.7",
        "platform": pmd.architecture,
        "supported_platform": (),
        "classifiers": list(pmd.classifiers()) + pmd.trove_license() + pmd.trove_status(),
        "provides": (),
        "requires": pmd.install_requires().get("install_requires") or (),
        "obsoletes": (),
        "project_urls": [f"{k}, {v}" for k, v in pmd.project_urls().items()],
        "provides_dist": (),
        "requires_dist": pmd.install_requires().get("install_requires") or (),
        "obsoletes_dist": (),
        "requires_external": (),
        "provides_extra": (),
    }
    print(meta)
    print(pmd.install_requires())

    # comment/readme
    for docs in pmd.plugin_doc(), psetup.get_readme():
        if docs["long_description"]:
            meta.update({  # with "long_" prefix cut off
                k[5:]: v for k, v in docs.items()
            })

    # entry_points are in ini file
    for section, entries in pmd.entry_points().items():
        ini.entrypoints[section] = ini.entrypoints.get(section, {})
        for script in entries:
            ini.entrypoints[section].update(
                dict(re.findall("(.+)=(.+)", script))
            )
    print(ini.entrypoints)

    # strip empty entries
    return {k: v for k, v in meta.items() if v}



#-- buildapi
from flit_core.buildapi import (     # These have to be late imports; else they'll
    get_requires_for_build_wheel,    # bind with the original buildapi functions.
    get_requires_for_build_sdist,
    get_requires_for_build_editable,
    prepare_metadata_for_build_wheel,
    prepare_metadata_for_build_editable,
    build_wheel,
    build_editable,
    build_sdist,
)

#-- invocation point
from flit import main

if __name__ == "__main__":
    main(sys.argv)
