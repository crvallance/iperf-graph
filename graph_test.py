from matplotlib import pyplot as plt
from matplotlib import style
import json
import pathlib
import argparse

parser = argparse.ArgumentParser(description='Somestuff!')
parser.add_argument("--f", nargs='*', help='Pass in the files to be graphed together')
# sum_stream = parser.add_mutually_exclusive_group(required=True)
sum_stream = parser.add_mutually_exclusive_group(required=False)
sum_stream.add_argument("--sum", action='store_true', help='Used to only graph sums')
sum_stream.add_argument("--stream", action='store_true', help='Used to graph each stream')
parser.add_argument("--title", help='Manually give the graph a title')


def in_progress(args):
    # style
    plt.style.use('seaborn-darkgrid')
    cp = 1
    for input_file in args.f:
        x = []
        y = []
        p = pathlib.Path(input_file)
        f = open(input_file)
        try:
            data = json.load(f)
        except:
            print(input_file)
            # raise
        # print(data['end'].keys())
        for item in data['intervals']:
            # print(item)
            # print('x is: ' + str(item['sum']['start']))
            x.append(item['sum']['start'])
            # print('y is: ' + str(item['sum']['bits_per_second']))
            y.append(item['sum']['bits_per_second'] / 8e+6)
        # create a color palette
        palette = plt.get_cmap('tab20b')
        plt.subplots_adjust(right=0.7)
        plt.plot(x, y, color=palette(cp), label=p.stem, linewidth=3)
        # plt.plot(x1,y1,'c',label='line two',linewidth=5)
        cp += 1
    if args.title:
        plt.title(args.title)
    else:
        plt.title('iPerf Data')
    plt.ylabel('Mbps')
    plt.xlabel('Time (Seconds)')
    plt.grid(True, color='k')
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.show()


'''
#use('ggplot')
x=[5,8,10]
y=[12,16,6]
x1=[6,9,11]
y1=[6,15,7]
plt.plot(x,y,'g',label='line one',linewidth=5)
plt.plot(x1,y1,'c',label='line two',linewidth=5)
plt.title('iPerf Data')
plt.ylabel('Bytes/Second')
plt.xlabel('Time (Seconds)')
plt.grid(True,color='K')
plt.legend()
plt.show()
'''

# https://www.probytes.net/blog/plotting-graphs-in-python/
# https://python-graph-gallery.com/124-spaghetti-plot/


def main():
    args = parser.parse_args()
    # files = args.f
    # print(args)
    in_progress(args)


if __name__ == "__main__":
    main()
