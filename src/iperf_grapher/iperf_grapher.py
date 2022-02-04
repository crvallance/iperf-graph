import json
import pathlib
import sys
from dataclasses import dataclass
from typing import Type

import click
from matplotlib import pyplot as plt
import tomli


@dataclass()
class ArgsShim():
    f: str
    title: str = None
    noshow: str = None
    label: str = None
    config: Type[pathlib.Path] = None


@click.command()
@click.argument('files', nargs=-1, type=click.Path(), required=True)
@click.option('--title', default='', type=str, help='Set graph title (use quotes for spaces)')
@click.option('--noshow', is_flag=True, default=False, help='Run without graphical preview')
@click.option('--config', default=None, type=click.Path(), help='Specify config file location other than current dir')
def new_args(**params):
    args = ArgsShim(f=params['files'])
    if params['title']:
        args.title = params['title']
    if params['noshow']:
        args.noshow = params['noshow']
    if params['config']:
        args.config = params['config']
    grapher(args)


def config_parse(filename: str) -> dict:
    try:
        with open(filename, "rb") as f:
            try:
                toml_dict = tomli.load(f)
            except tomli.TOMLDecodeError:
                print("TOML File is not valid")
    except FileNotFoundError as err:
        print(f'{err}')
        sys.exit(2)
    return(toml_dict)


def label_tokenization(data_filename: str, config_filename: str = 'conf.toml') -> str:
    label = ''
    settings = config_parse(config_filename)
    delim = settings['token_map']['delimiter']
    filename_chunks = data_filename.split(delim)
    data_list = settings['token_map']['label_order']
    for i, data in enumerate(data_list):
        position = settings['token_map'][data]
        label_part = filename_chunks[position]
        if i != len(data_list) - 1:
            label += f'{label_part} '
        else:
            label += f'{label_part}'
    return(label)


def grapher(args: Type[ArgsShim]):
    # style
    plt.style.use('seaborn-darkgrid')
    cp = 1
    for input_file in args.f:
        x = []
        y = []
        bare_file = pathlib.Path(input_file).stem
        if args.config:
            label = label_tokenization(bare_file, args.config)
        else:
            label = label_tokenization(bare_file)
        f = open(input_file)
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(e)
            sys.exit(input_file + ' has a JSON error')
        for item in data['intervals']:
            x.append(item['sum']['start'])
            y.append(item['sum']['bits_per_second'] / 8e+6)
        # create a color palette
        palette = plt.get_cmap('tab20b')
        plt.subplots_adjust(right=0.7)
        plt.plot(x, y, color=palette(cp), label=label, linewidth=3)
        cp += 1
    if args.title:
        plt.title(args.title)
    else:
        plt.title('iPerf Data')
    plt.ylabel('Mbps')
    plt.xlabel('Time (Seconds)')
    plt.grid(True, color='k')
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    if args.noshow:
        imagefile = f.name.replace('json', 'png')
        plt.savefig(imagefile)
    else:
        plt.show()


def main():
    new_args()


if __name__ == "__main__":
    main()