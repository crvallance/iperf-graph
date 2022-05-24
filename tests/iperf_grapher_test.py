import pathlib
import hashlib

import pytest
from src.iperf_grapher.iperf_grapher import ArgsShim, grapher, file_extension_check, config_parse


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

@pytest.fixture
def bad_config_file_setup(tmp_path):
    config_file = tmp_path / 'file.txt'
    config_file.write_text('bad data')
    return(config_file)

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


def test_file_extension_check():
    ok_file_path = pathlib.Path('im-a-file')
    good_file_path = pathlib.Path('im-another-file.png')
    assert file_extension_check(ok_file_path) == pathlib.Path('im-a-file.png')
    assert file_extension_check(good_file_path) == pathlib.Path('im-another-file.png')
    with pytest.raises(AttributeError):
        file_extension_check('bad_string')

def test_config_parse(bad_config_file_setup):
    with pytest.raises(SystemExit):
        config_parse(bad_config_file_setup)
    good_config = pathlib.Path(f'./examples/conf.toml')
    toml_dict = {'token_map': {'Client': 0, 'Distance': 1, 'UL-DL': 2, 'label_order': ['Client', 'UL-DL', 'Distance'], 'delimiter': '_'}, 'optional': {}}
    assert config_parse(good_config) == toml_dict
    no_such_file = pathlib.Path('I-am-not-real.txt')
    with pytest.raises(SystemExit):
        config_parse(no_such_file)
