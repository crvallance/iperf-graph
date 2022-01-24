import pathlib
import subprocess


def test_help():
    help_cmd = subprocess.run(['python3', 'iperf_grapher.py', '--help'], capture_output=True, text=True)
    assert help_cmd.returncode == 0


def test_noshow():
    sum_cmd = subprocess.run(['python3', 'iperf_grapher.py', 'examples/laptop_0ft_R.json', '--noshow'], capture_output=True, text=True)
    assert sum_cmd.returncode == 0
    file = pathlib.Path("examples/laptop_0ft_R.png")
    assert file.exists()
    file.unlink()


def test_title():
    sum_cmd = subprocess.run(['python3', 'iperf_grapher.py', 'examples/laptop_0ft_R.json', '--noshow', '--title', 'the title'], capture_output=True, text=True)
    assert sum_cmd.returncode == 0
    file = pathlib.Path("examples/laptop_0ft_R.png")
    assert file.exists()
    file.unlink()


def test_show():
    sum_cmd = subprocess.run(['python3', 'iperf_grapher.py', 'examples/laptop_0ft_R.json'], capture_output=True, text=True)
    warning = 'UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.'
    assert warning in sum_cmd.stderr
