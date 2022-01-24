import pathlib

from iperf_grapher import ArgsShim, in_progress


def test_in_progress():
    example_file = 'laptop_0ft_S'
    args = ArgsShim(f=[f'./examples/{example_file}.json'])
    args.noshow = True
    in_progress(args)
    outfile = pathlib.Path(f'./examples/{example_file}.png')
    assert outfile.exists()
    outfile.unlink()
