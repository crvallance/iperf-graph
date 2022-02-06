import pathlib
import hashlib

import pytest
from src.iperf_grapher.iperf_grapher import ArgsShim, grapher


def hasher(filename):
    with open(filename, "rb") as f:
        file_hash = hashlib.blake2b()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return(file_hash.hexdigest())


@pytest.fixture
def arg_setup():
    example_file = 'laptop_0ft_S'
    args = ArgsShim(f=[f'./examples/{example_file}.json'])
    return(example_file, args)


def test_grapher(arg_setup):
    example_file, args = arg_setup
    args.noshow = True
    grapher(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    blake2b_hash = '659b6f5fba3bf14fac8fbe3b8dd63e0df554435d888f6102df70d6123253d8bb3b817b0dd2b432f2c745c8c820a3288a1349bc3947d3d7a3766a8b597698a58b'
    calc_hash = hasher(outfile)
    assert calc_hash == blake2b_hash
    outfile.unlink()
