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
    args.noshow = True
    args.config = pathlib.Path(f'./examples/conf.toml')
    return(example_file, args)


def test_grapher_Mbps(arg_setup):
    example_file, args = arg_setup
    grapher(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    blake2b_hash = 'a0a323e58ff4e40953c3c6180db4dc7496137b54279ed17924781ecf375918714f0a593c93d3d78ac535d2b7a5e645440791f43e078e4c0d25a8ae5d1f20a769'
    calc_hash = hasher(outfile)
    assert calc_hash == blake2b_hash
    outfile.unlink()


def test_grapher_MBps(arg_setup):
    example_file, args = arg_setup
    args.speed_unit = 'MBps'
    grapher(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    blake2b_hash = 'a66e6c997e4d75b63b8aea6cf2f0c24ba795ab0761d8bbb8315a81df8d5e296f0b593dc2f0c5c926b783a88cca83a86ced1a09fd520942e421d2853199e6ad24'
    calc_hash = hasher(outfile)
    assert calc_hash == blake2b_hash
    outfile.unlink()


def test_grapher_Gbps(arg_setup):
    example_file, args = arg_setup
    args.speed_unit = 'Gbps'
    grapher(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    blake2b_hash = '8404ae0d23110e216ee29f25c32e24eea084c327f5e40d41e46a9fc2409d3e681487e158e389764443f4ee57166da679bed615f5bd14738e1a33c914531ad6ae'
    calc_hash = hasher(outfile)
    assert calc_hash == blake2b_hash
    outfile.unlink()
