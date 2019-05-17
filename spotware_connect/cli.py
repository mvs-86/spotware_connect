# -*- coding: utf-8 -*-

"""Console script for {{cookiecutter.project_slug}}."""
import sys
import click


@click.group()
def main():
    pass


@click.command()
def fix_imports():
    import re

    path = "./spotware_connect/protobuf/"
    file_names = ("OpenApiCommonMessages_pb2", "OpenApiMessages_pb2")
    for fn in file_names:
        pyfile = path + fn + ".py"
        content = ""
        with open(pyfile) as f:
            content = f.read()

        if re.search("from . import Open.*", content):
            continue

        with open(pyfile, "w") as f:
            new_text = content.replace('import Open', 'from . import Open')
            f.write(new_text)


@click.command()
def create_requests():
    from jinja2 import Environment, PackageLoader
    from spotware_connect import protobuf as pb

    env = Environment(
        loader=PackageLoader('spotware_connect', 'templates'),
        trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template('requests.py.j2')
    protobufs_with_fields = pb.describe_fields(pb.getReqPayloads())
    template.stream(protobufs=protobufs_with_fields).dump("./spotware_connect/requests.py")

@click.command()
def create_responses():
    from jinja2 import Environment, PackageLoader
    from spotware_connect import protobuf as pb

    env = Environment(
        loader=PackageLoader('spotware_connect', 'templates'),
        trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template('responses.py.j2')
    protobufs_with_fields = pb.describe_fields(pb.getResPayloads() + pb.getEventPayloads())
    template.stream(protobufs=protobufs_with_fields).dump("./spotware_connect/responses.py")


main.add_command(fix_imports)
main.add_command(create_requests)
main.add_command(create_responses)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
