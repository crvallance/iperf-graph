from rich.prompt import Prompt
import tomli_w
import tomli


def core():
    options = ['Client', 'UL-DL', 'Distance', 'Ignore']
    parsed_file = ['laptop', '0ft', 'R', 'Hi', 'What', 'CV']
    stored = {}
    for i, _ in enumerate(parsed_file):
        # pos = 'position_' + str(i)
        data = Prompt.ask(f"What do you want to map {_} to?", choices=options)
        if 'Ignore' in data:
            continue
        stored[data] = i

    print(stored)
    config_toml = {"token_map": stored}
    with open("conf3.toml", "wb") as f:
        tomli_w.dump(config_toml, f)


def main():
    with open("conf.toml", "rb") as f:
        try:
            toml_dict = tomli.load(f)
        except tomli.TOMLDecodeError:
            print("TOML File is not valid")

    print(toml_dict)


if __name__ == '__main__':
    main()
    # core()
