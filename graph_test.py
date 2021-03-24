from matplotlib import pyplot as plt
from matplotlib import style
import json
import pathlib
import argparse
import re
import sys

parser = argparse.ArgumentParser(description='Somestuff!')
parser.add_argument("--f", nargs='*', help='Pass in the files to be graphed together')
# sum_stream = parser.add_mutually_exclusive_group(required=True)
sum_stream = parser.add_mutually_exclusive_group(required=False)
sum_stream.add_argument("--sum", action='store_true', help='Used to only graph sums')
sum_stream.add_argument("--stream", action='store_true', help='Used to graph each stream')
parser.add_argument("--title", help='Manually give the graph a title')
key_parse = parser.add_argument_group()
key_parse.add_argument("--kd", help='Designate a delimeter for filename to key parsing')
key_parse.add_argument("--km", help='"Mask" for new desired output of key name.  Use numbers to designate order, omit fields, and additional text as needed.\nExample: "1 2 4 small 3" would produce "cat dog snake small fish" from a file called "cat_dog_fish_snake.json"')
parser.add_argument("--noshow", action='store_const', const=True, help='Save to file without showing output')

def key_parse(args, coded_name):
    pattern = re.compile(r'([0-9])')
    delim = args.kd
    mask = args.km
    result = mask
    try:
        elements = coded_name.split(delim)
    except:
        print('Something wrong')
        raise
    for m in re.finditer(pattern, mask):
        mask_pos = m.group(1)
        p = re.compile(str(mask_pos))
        file_pos = int(m.group(1))-1
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
    args = parser.parse_args()
    in_progress(args)


if __name__ == "__main__":
    main()
