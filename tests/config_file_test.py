import pytest
import pathlib
from src.iperf_grapher.config_file import Config, TokenMapConfig, TomlReader

def test_config():
    configfile = pathlib.Path(f'./examples/conf.toml')
    config = Config(configfile)
    assert config.config_item.delimiter == '_'
    assert config.config_item.tokens == {'Client': 0, 'Distance': 1, 'UL-DL': 2}
    assert config.config_item.label_order == ["Client", "UL-DL", "Distance"]