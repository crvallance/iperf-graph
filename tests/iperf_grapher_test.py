import pathlib

import pytest
from iperf_grapher import ArgsShim, in_progress, key_parse


@pytest.fixture
def arg_setup():
    example_file = 'laptop_0ft_S'
    args = ArgsShim(f=[f'./examples/{example_file}.json'])
    return(example_file, args)


def test_in_progress(arg_setup):
    example_file, args = arg_setup
    args.noshow = True
    in_progress(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    outfile.unlink()


def test_key_parse(arg_setup):
    example_file, args = arg_setup
    args.kd = '_'
    args.km = '1 2 3 monkey'
    p = pathlib.Path(args.f[0])
    coded_name = p.stem
    result = key_parse(args, coded_name)
    assert result == 'laptop 0ft S monkey'
