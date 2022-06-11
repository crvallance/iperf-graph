import pathlib
import subprocess
import pytest


def test_help():
    help_cmd = subprocess.run(['python3', 'src/iperf_grapher/iperf_grapher.py', '--help'], capture_output=True, text=True)
    assert help_cmd.returncode == 0

def test_noshow():
    sum_cmd = subprocess.run(['python3', 'src/iperf_grapher/iperf_grapher.py', 'examples/laptop_0ft_R.json', '--noshow', '--config', './examples/conf.toml'], capture_output=True, text=True)
    assert sum_cmd.returncode == 0
    file = pathlib.Path("examples/laptop_0ft_R.png")
    assert file.exists()
    file.unlink()

def test_title():
    sum_cmd = subprocess.run(['python3', 'src/iperf_grapher/iperf_grapher.py', 'examples/laptop_0ft_R.json', '--noshow', '--title', 'the title', '--config', './examples/conf.toml'], capture_output=True, text=True)
    assert sum_cmd.returncode == 0
    file = pathlib.Path("examples/laptop_0ft_R.png")
    assert file.exists()
    file.unlink()

@pytest.mark.xfail
def test_show():
    sum_cmd = subprocess.run(['python3', 'src/iperf_grapher/iperf_grapher.py', 'examples/laptop_0ft_R.json', '--config', './examples/conf.toml'], capture_output=True, text=True)
    warning = 'UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.'
    assert warning in sum_cmd.stderr

def test_config():
    sum_cmd = subprocess.run(['python3', 'src/iperf_grapher/iperf_grapher.py', 'examples/laptop_0ft_R.json', '--config', './examples/conf.toml'], capture_output=True, text=True)
    assert sum_cmd.returncode == 0
    borked_cmd = subprocess.run(['python3', 'src/iperf_grapher/iperf_grapher.py', 'examples/laptop_0ft_R.json', '--config', './does-not-exist/conf.toml'], capture_output=True, text=True)
    assert borked_cmd.returncode == 1
    warning = "[Errno 2] No such file or directory: 'does-not-exist/conf.toml'\n"
    # warning = "[Errno 2] No such file or directory: './does-not-exist/conf.toml'"
    assert warning in borked_cmd.stdout
