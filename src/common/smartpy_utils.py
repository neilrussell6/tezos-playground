"""Common SmartPy Utils"""

import subprocess
import os
from os.path import dirname, join
from functools import partial

from src.common.pytest_utils import cached
from src.common.path_utils import splitall
from src.common.logging_decorators import debug


@debug
def compile_smartpy_to_smlse(output_name, contract_cls, target_dir):
    """Compile from SMLSE to Michelson and Micheline and return Micheline path."""
    contract = contract_cls()
    target_smlse = join(target_dir, '_{}.smlse'.format(output_name))
    open(target_smlse, 'w').write(contract.export())
    return target_smlse


@debug
def compile_smlse_to_michelson_and_micheline(output_name, target_smlse, target_dir):
    """Compile from SMLSE to Michelson and Micheline and return Micheline path."""
    command = ['node', os.environ['SMARTPY_BASIC_JS_PATH']]
    for (opt, arg) in [('--compile', target_smlse), ('--outputDir', target_dir)]:
        command += [opt, arg]
    subprocess.run(command)
    return '_{}.tz'.format(output_name)


@debug
def _compile_smartpy_to_micheline(target_dir, output_name, contract_cls, file_path):
    """Compile from SmartPy to Micheline and return Micheline path."""
    smlse_path = compile_smartpy_to_smlse(output_name, contract_cls, target_dir)
    micheline_path = compile_smlse_to_michelson_and_micheline(output_name, smlse_path, target_dir)
    return join(dirname(file_path), micheline_path)


@debug
def compile_smartpy_to_micheline(output_name, contract_cls, file_path, cache=None):
    """Compile from SmartPy to Micheline and return Micheline path or return cached Micheline path."""
    target_dir = dirname(file_path)
    f = partial(_compile_smartpy_to_micheline, target_dir, output_name, contract_cls, file_path)
    if cache is None:
        return f()
    cache_key = '/'.join(splitall(file_path)[-4:]).replace('.py', '')
    return cached(cache, cache_key, f)
