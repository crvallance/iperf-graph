import json
import pathlib
import re
import sys
from dataclasses import dataclass

import click
from matplotlib import pyplot as plt


@dataclass()
class ArgsShim():
    f: str
    title: str = None
    noshow: str = None
    kd: str = None
    km: str = None


@click.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--title', default='', type=str)
@click.option('--noshow', is_flag=True, default=False)
def new_args(**params):
    # print(params['files'])
    args = ArgsShim(f=params['files'])
    if params['title']:
        args.title = params['title']
    if params['noshow']:
        args.noshow = params['noshow']
    in_progress(args)


def key_parse(args, coded_name):
    pattern = re.compile(r'([0-9])')
    delim = args.kd
    mask = args.km
    result = mask
    try:
        elements = coded_name.split(delim)
    except ValueError as N:
        print(f'Something wrong: {N}')
        raise
    for m in re.finditer(pattern, mask):
        mask_pos = m.group(1)
        p = re.compile(str(mask_pos))
        file_pos = int(m.group(1)) - 1
        result = p.sub(elements[file_pos], result, count=1)
    return(result)


def in_progress(args):
    # style
    plt.style.use('seaborn-darkgrid')
    cp = 1
    for input_file in args.f:
        x = []
        y = []
        p = pathlib.Path(input_file)
        if args.kd and args.km:
            label = key_parse(args, p.stem)
        else:
            label = p.stem
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
