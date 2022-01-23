import pathlib
import subprocess


def test_help():
    help_cmd = subprocess.run(['python3', 'graph_test.py', '--help'], capture_output=True, text=True)
    assert help_cmd.returncode == 0


def test_sum():
    sum_cmd = subprocess.run(['python3', 'graph_test.py', '--f', 'examples/laptop_0ft_R.json', '--sum', '--noshow'], capture_output=True, text=True)
    assert sum_cmd.returncode == 0
    file = pathlib.Path("examples/laptop_0ft_R.png")
    assert file.exists()
    file.unlink()
