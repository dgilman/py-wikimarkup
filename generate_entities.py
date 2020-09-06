import requests


def main():
    resp = requests.get("https://html.spec.whatwg.org/entities.json")
    resp.raise_for_status()
    resp = resp.json()

    names = set()

    output = "# Generated by generate_entities.py - do not edit!\n\n"
    output += "html_entities = {\n"
    for entity in resp:
        name = entity
        if name.startswith("&"):
            name = name[1:]
        if name.endswith(";"):
            name = name[:-1]

        if name in names:
            continue
        names.add(name)

        chars = resp[entity]["characters"].encode("unicode_escape").decode('ascii')
        if '"' in chars:
            chars = chars.replace('"', '\\"')
        output += f'    "{name}": "{chars}",\n'
    output += "}\n"

    with open("wikimarkup/entities.py", "w") as fd:
        fd.write(output)


if __name__ == "__main__":
    main()