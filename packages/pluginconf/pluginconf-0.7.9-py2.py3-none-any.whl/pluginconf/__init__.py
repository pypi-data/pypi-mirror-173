# encoding: utf-8
# api: python
##type: extract
# category: config
# title: Plugin configuration
# description: Read meta data, pyz/package contents, module locating
# version: 0.7.9
# state: stable
# classifiers: documentation
# depends: python >= 2.7
# suggests: python:flit, python:PySimpleGUI
# license: PD
# priority: core
# api-docs: https://fossil.include-once.org/pluginspec/doc/trunk/html/index.html
# docs: https://fossil.include-once.org/pluginspec/
# url: http://fossil.include-once.org/streamtuner2/wiki/plugin+meta+data
# config: -
# format: off
# pylint: disable=invalid-name
# console-scripts: flit-pluginconf=pluginconf.flit:main, pluginconf.flit=pluginconf.flit:main
#
# Provides plugin lookup and meta data extraction utility functions.
# It's used to abstract module+option management in applications.
# For consolidating internal use and external/tool accessibility.
#
# The key:value format is language-agnostic. It's basically YAML in
# a topmost script comment. For Python only # hash comments though.
# Uses common field names, a documentation block, and an obvious
# `config: { .. }` spec for options and defaults.
#
# It neither imposes a specific module/plugin API, nor config storage,
# and doesn't fixate module loading. It's really just meant to look
# up meta infos.
# This approach avoids in-code values/inspection, externalized meta
# descriptors, and any hodgepodge or premature module loading just to
# uncover module description fields.
#
# plugin_meta()
# ‾‾‾‾‾‾‾‾‾‾‾‾‾
#  Is the primary function to extract a meta dictionary from files.
#  It either reads from a given module= name, a literal fn=, or just
#  src= code, and as fallback inspects the last stack frame= else.
#
# module_list()
# ‾‾‾‾‾‾‾‾‾‾‾‾‾
#  Returns basenames of available/installed plugins. It uses the
#  plugin_base=[] list for module relation. Which needs to be set up
#  beforehand, or injected.
#
# add_plugin_defaults()
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#  Populates a config_options{} and plugin_states{} list. Used for
#  initial setup, or when adding new plugins, etc. Both dicts might
#  also be ConfigParser stores, or implement magic __set__ handling
#  to act on state changes.
#
# get_data()
# ‾‾‾‾‾‾‾‾‾‾
#  Is mostly an alias for pkgutil.get_data(). It abstracts the main
#  base path, allows PYZ usage, and adds some convenience flags.‾
#  It's somewhat off-scope for plugin management, but used internally.
#
# argparse_map()
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#  Converts a list of config: options with arg: attribute for use as
#  argparser parameters.
#
#
# Generally this scheme concerns itself more with plugin basenames.
# That is: module scripts in a package like `ext.plg1` and `ext.plg2`.
# It can be initialized by injecting the plugin-package basename into
# plugin_base = []. The associated paths will be used for module
# lookup via pkgutil.iter_modules().
#
# Ideally a designated reference base_module should be extended with
# new lookup locations via `module.__path__ += ["./local"]` for exmple.
# Plugin loading thus becomes as simple as __import__("ext.local").
#
# Using a plugin_state config dictionary in most cases can just list
# module basenames, if there's only one namespace to manage. (Plugin
# names unique across project.)

""" Plugin meta extraction and module lookup"""


import sys
import os
import re
import functools
import pkgutil
import inspect
try:
    from gzip import decompress as gzip_decode  # Py3 only
except ImportError:
    try:
        from compat2and3 import gzip_decode   # st2 stub
    except ImportError:
        import zlib
        def gzip_decode(bytestr):
            """ haphazard workaround """
            return zlib.decompress(bytestr, 16 + zlib.MAX_WBITS)
import zipfile
import argparse

__all__ = [
    "get_data", "module_list", "plugin_meta", "add_plugin_defaults"
]


# Injectables
# ‾‾‾‾‾‾‾‾‾‾‾
""" injectable callback function for logging """
log_ERR = lambda *x: None

"""
File lookup relation for get_data(), should name a top-level package.
(Equivalent PluginBase(package=…))
"""
module_base = "config"

"""
Package/module names for module_list() and plugin_meta() lookups.
All associated paths will be scanned for module/plugin basenames.
(Equivalent to `searchpath` in PluginBase)
"""
plugin_base = ["channels"]

""" normalize config type: names to `str`, `text`, `bool`, `int`, `select`, `dict` """
config_opt_type_map = {
    "longstr": "text",
    "string": "str",
    "boolean": "bool",
    "checkbox": "bool",
    "integer": "int",
    "number": "int",
    "choice": "select",
    "options": "select",
    "table": "dict",
    "array": "dict"
}


# Compatiblity
# ‾‾‾‾‾‾‾‾‾‾‾‾
def renamed_arguments(renamed):
    """ map old argument names """
    def wrapped(func):
        def execute(*args, **kwargs):
            return func(*args, **{
                renamed.get(key, key): value
                for key, value in kwargs.items()
            })
        functools.update_wrapper(execute, func)
        return execute
    return wrapped


# Resource retrieval
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
@renamed_arguments({"fn": "filename", "gz": "gzip"})
def get_data(filename, decode=False, gzip=False, file_base=None):
    """
    Fetches file content from install path or from within PYZ
    archive. This is just an alias and convenience wrapper for
    pkgutil.get_data().
    Utilizes the module_base / plugin_base as top-level reference.

    Parameters
    ----------
    filename :  str
        filename in pyz or bundle
    decode : bool
        text file decoding utf-8
    gzip : bool
        automatic gzdecode
    file_base : list
        alternative base module reference

    Returns
    -------
    str : file contents
    """
    try:
        data = pkgutil.get_data(file_base or module_base, filename)
        if gzip:
            data = gzip_decode(data)
        if decode:
            return data.decode("utf-8", errors='ignore')
        return str(data)
    except:
        # log_ERR("get_data() didn't find:", fn, "in", file_base)
        pass


# Plugin name lookup
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
def module_list(extra_paths=None):
    """
    Search through ./plugins/ (and other configured plugin_base
    names → paths) and get module basenames.

    Parameters
    ----------
    extra_paths : list
        in addition to plugin_base list

    Returns
    -------
    list : names of found plugins
    """

    # Convert plugin_base package names into paths for iter_modules
    paths = []
    for module_or_path in plugin_base:
        if sys.modules.get(module_or_path):
            paths += sys.modules[module_or_path].__path__
        elif os.path.exists(module_or_path):
            paths.append(module_or_path)

    # Should list plugins within zips as well as local paths
    dirs = pkgutil.iter_modules(paths + (extra_paths or []))
    return [name for loader, name, ispkg in dirs]


# Plugin => meta dict
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
def all_plugin_meta():
    """
    This is a trivial wrapper to assemble a complete dictionary
    of available/installed plugins. It associates each plugin name
    with a its meta{} fields.

    Returns
    -------
    dict : names to meta data dict
    """
    return {
        name: plugin_meta(module=name) for name in module_list()
    }


# Plugin meta data extraction
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
@renamed_arguments({"fn": "filename"})
def plugin_meta(filename=None, src=None, module=None, frame=1, **kwargs):
    """
    Extract plugin meta data block from different sources:

    Parameters
    ----------
    filename : str
        read literal files, or .pyz contents
    src : str
        from already uncovered script code
    module : str
        lookup per pkgutil, from plugin_base or top-level modules
    frame : int
        extract comment header of caller (default)
    extra_base : list
        additional search directories
    max_length : list
        maximum size to read from files

    Returns
    -------
    dict : key-value pairs of comment fields, config: preparsed
    """

    # Try via pkgutil first,
    # find any plugins.* modules, or main packages
    if module:
        filename = module
        for base in plugin_base + kwargs.get("extra_base", []):
            try:
                src = get_data(filename=filename+".py", decode=True, file_base=base)
                if src:
                    break
            except:
                continue  # plugin_meta_extract() will print a notice later

    # Real filename/path
    elif filename and os.path.exists(filename):
        src = open(filename).read(kwargs.get("max_length", 6144))

    # Else get source directly from caller
    elif not src and not filename:
        module = inspect.getmodule(sys._getframe(frame+1)) # decorator+1
        filename = inspect.getsourcefile(module)
        src = inspect.getcomments(module)

    # Assume it's a filename matches …/base.zip/…/int.py
    elif filename:
        int_fn = ""
        while len(filename) and not os.path.exists(filename): # pylint: disable=len-as-condition
            filename, add = os.path.split(filename)
            int_fn = add + "/" + int_fn
        if len(filename) >= 3 and int_fn and zipfile.is_zipfile(filename):
            src = zipfile.ZipFile(filename, "r").read(int_fn.strip("/"))

    # Extract source comment into meta dict
    if not src:
        src = ""
    if not isinstance(src, str):
        src = src.decode("utf-8", errors='replace')
    return plugin_meta_extract(src, filename)


# Comment and field extraction logic
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
@renamed_arguments({"fn": "filename"})
def plugin_meta_extract(src="", filename=None, literal=False):
    """
    Finds the first comment block. Splits key:value header
    fields from comment. Turns everything into an dict, with
    some stub fields if absent.

    Parameters
    ----------
    src : str
        from existing source code
    filename : str
        set filename attribute
    literls : bool
        just split comment from doc
    """

    # Defaults
    meta = {
        "id": os.path.splitext(os.path.basename(filename or ""))[0],
        "fn": filename,
        "api": "python",
        "type": "module",
        "category": None,
        "priority": None,
        "version": "0",
        "title": filename,
        "description": "no description",
        "config": [],
        "doc": ""
    }

    # Extract coherent comment block
    src = src.replace("\r", "")
    if not literal:
        src = rx.comment.search(src)
        if not src:
            log_ERR("Couldn't read source meta information:", filename)
            return meta
        src = src.group(0)
        src = rx.hash.sub("", src).strip()

    # Split comment block
    if src.find("\n\n") > 0:
        src, meta["doc"] = src.split("\n\n", 1)

    # Turn key:value lines into dictionary
    for field in rx.keyval.findall(src):
        meta[field[0].replace("-", "_")] = field[1].strip()
    meta["config"] = plugin_meta_config(meta.get("config") or "")

    return PluginMeta(meta)


# Dict wrapper
# ‾‾‾‾‾‾‾‾‾‾‾‾
class PluginMeta(dict):
    """ Plugin meta data, convenience dict with property access """

    def __getattr__(self, key):
        """ Return [key] for .property access, else None """
        return self.get(key)

    def __hasattr__(self, key):
        """ Return [key] for .property access, else None """
        return key in self


# Unpack config: structures
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
def plugin_meta_config(src):
    """
    Further breaks up the meta['config'] descriptor.
    Creates an array from JSON/YAML option lists.

    Stubs out name, value, type, description if absent.
    # config:
       { name: 'var1', type: text, value: "default, ..." }
       { name=option2, type=boolean, $value=1, etc. }

    Parameters
    ----------
    src : str
        unprocessed config: field

    Returns
    -------
    list : of option dictionaries
    """

    config = []
    for entry in rx.config.findall(src):
        entry = entry[0] or entry[1]
        opt = {
            "type": None,
            "name": None,
            "description": "",
            "value": None
        }
        for field in rx.options.findall(entry):
            opt[field[0]] = (field[1] or field[2] or field[3] or "").strip()
        # normalize type
        opt["type"] = config_opt_type_map.get(opt["type"], opt["type"] or "str")
        # preparse select:
        if opt.get("select"):
            opt["select"] = config_opt_parse_select(opt.get("select", ""))
        config.append(opt)
    return config

# split up `select: 1=on|2=more|3=title` or `select: foo|bar|lists`
def config_opt_parse_select(select):
    """ unpack 1|2|3 or title=lists """
    if re.search("([=:])", select):
        return dict(rx.select_dict.findall(select))
    #else:
    return {val: val for val in rx.select_list.findall(select)}


# Comment extraction regexps
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
class rx:
    """
    Pretty crude comment splitting approach. But works
    well enough already. Technically a YAML parser would
    do better; but is likely overkill.
    """

    comment = re.compile(r"""(^ {0,4}#.*\n)+""", re.M)
    hash = re.compile(r"""(^ {0,4}#{1,2} {0,3}\r*)""", re.M)
    keyval = re.compile(r"""
        ^([\w-]+):(.*$(?:\n(?![\w-]+:).+$)*)   # plain key:value lines
    """, re.M | re.X)
    config = re.compile(r"""
        \{ ((?: [^\{\}]+ | \{[^\}]*\} )+) \}   # JSOL/YAML scheme {...} dicts
        | \< (.+?) \>                          # old <input> HTML style
    """, re.X)
    options = re.compile(r"""
        ["':$]?   (\w*)  ["']?                 # key or ":key" or '$key'
        \s* [:=] \s*                           # "=" or ":"
     (?:  "  ([^"]*)  "
       |  '  ([^']*)  '                        #  "quoted" or 'singl' values
       |     ([^,]*)                           #  or unquoted literals
     )
    """, re.X)
    select_dict = re.compile(r"(\w+)\s*[=:>]+\s*([^=,|:]+)")
    select_list = re.compile(r"\s*([^,|;]+)\s*")



# ArgumentParser options conversion
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
def argparse_map(opt):
    """
    As variation of in-application config: options, this method converts
    cmdline argument specifiers.

    # config:
       { arg: -i, name: input[], type: str, description: input files }

    Which allows to collect argumentparser options from different plugins.
    The only difference to normal config entries is the `arg:` attribute.

     · It adds array arguments with a [] name suffix, or a `*` type suffix.
       Else even a `?` or `+` and numeric counts after the type flag.
     · Understands the types `str`, `int` and `bool`.
     · Entries may carry a `hidden: 1` or `required: 1` attribute.
     · And `help:` is an alias to `description:`
       And `default:` an alias for `value:`
     · While `type: select` utilizes the `select: a|b|c` format as usual.

    ArgParsers const=, metavar= flag, or type=file are not aliased here.
    Basically returns a dictionary that can be fed per **kwargs directly
    to an ArgumentParsers add_argument(). Iterate over each plugins
    meta['config'][] options to convert them.
    """
    if not ("arg" in opt and opt["name"] and opt["type"]):
        return {}

    # Extract --flag names
    args = opt["arg"].split() + re.findall(r"-+\w+", opt["name"])

    # Prepare mapping options
    typing = re.findall(r"bool|str|\[\]|const|false|true", opt["type"])
    naming = re.findall(r"\[\]", opt["name"])
    name = re.findall(r"(?<!-)\b\w+", opt["name"])
    nargs = re.findall(r"\b\d+\b|[\?\*\+]", opt["type"]) or [None]
    is_arr = "[]" in (naming + typing) and nargs == [None]
    is_bool = "bool" in typing
    false_b = "false" in typing or opt["value"] in ("0", "false")
    # print("\nname=", name, "is_arr=", is_arr, "is_bool=", is_bool,
    # "bool_d=", false_b, "naming=", naming, "typing=", typing)

    # Populate combination as far as ArgumentParser permits
    # pylint: disable=bad-whitespace, bad-continuation
    kwargs = dict(
        args     = args,
        dest     = name[0] if not name[0] in args else None,
        action   = is_arr and "append"
                   or  is_bool and false_b and "store_false"
                   or  is_bool and "store_true"  or  "store",
        nargs    = nargs[0],
        default  = opt.get("default") or opt["value"],
        type     = None if is_bool  else  ("int" in typing and int
                   or  "bool" in typing and bool  or  str),
        choices  = opt["select"].split("|") if "select" in opt else None,
        required = "required" in opt or None,
        help     = opt["description"] if not "hidden" in opt
                   else argparse.SUPPRESS
    )
    return {k: w for k, w in kwargs.items() if w is not None}


# Add plugin defaults to conf.* store
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
def add_plugin_defaults(conf_options, conf_plugins, meta, module=""):
    """
    Utility function which collect defaults from plugin meta data to
    a config store. Which in the case of streamtuner2 is really just a
    dictionary `conf{}` and a plugin list in `conf.plugins{}`.

    Parameters
    ----------
    conf_options : dict : input/output
        storage for amassed options
    conf_plugins : dict : input/output
        enable status based on plugin state/priority:
    meta : dict
        input plugin meta data (invoke once per plugin)
    module : str
        basename of meta: blocks plugin file
    """

    # Option defaults, if not yet defined
    for opt in meta.get("config", []):
        if "name" not in opt or "value" not in opt:
            continue
        _value = opt.get("value", "")
        _name = opt.get("name")
        _type = opt.get("type")
        if _name in conf_options:
            continue
        # typemap
        if _type == "bool":
            val = _value.lower() in ("1", "true", "yes", "on")
        elif _type == "int":
            val = int(_value)
        elif _type in ("table", "list"):
            val = [
                re.split(r"\s*[,;]\s*", s.strip())
                for s in re.split(r"\s*[|]\s*", _value)
            ]
        elif _type == "dict":
            val = dict([
                re.split(r"\s*(?:=>+|==*|-+>|:=+)\s*", s.strip(), 1)
                for s in re.split(r"\s*[|;,]\s*", _value)
            ])
        else:
            val = str(_value)
        conf_options[_name] = val

    # Initial plugin activation status
    if module and module not in conf_plugins:
        conf_plugins[module] = meta.get("priority") in (
            "core", "builtin", "always", "default", "standard"
        )
