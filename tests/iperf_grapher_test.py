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
    args.config = pathlib.Path('./examples/conf.toml')
    return(example_file, args)


def test_grapher_Mbps(arg_setup):
    example_file, args = arg_setup
    grapher(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    blake2b_hash = '64f97f6eee33bf32f02db5c60013c09178d7c5f99212e90b7e5e49a30cb10ec738ff8adcd1fbeac644228753d895b1df86f277486ce4052abc68a8032cae0628'
    calc_hash = hasher(outfile)
    assert calc_hash == blake2b_hash
    outfile.unlink()


def test_grapher_MBps(arg_setup):
    example_file, args = arg_setup
    args.speed_unit = 'MBps'
    grapher(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    blake2b_hash = 'cbaad0799f6250954786fca0c5e717a3a0a95e05a785277f80282c1f3fa3a7d8a1314495be4b94e4c2de4de86e5a20df67703d5fdb272dabb9eace76ec08227c'
    calc_hash = hasher(outfile)
    assert calc_hash == blake2b_hash
    outfile.unlink()


def test_grapher_Gbps(arg_setup):
    example_file, args = arg_setup
    args.speed_unit = 'Gbps'
    grapher(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    blake2b_hash = 'a2d49e50c14fe6b1aff0291702b6665e0b9ff098e31d47c9036dd450bd6ae6cb26f90398fddd21028069562f5e3dd760c06d15d60f12cb51c13c5c4b16740526'
    calc_hash = hasher(outfile)
    assert calc_hash == blake2b_hash
    outfile.unlink()
