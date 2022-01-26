import pathlib

import pytest
from iperf_grapher import ArgsShim, grapher


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
    outfile.unlink()
