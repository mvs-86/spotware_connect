# -*- coding: utf-8 -*-

"""Console script for {{cookiecutter.project_slug}}."""

import click


@click.command()  # pragma: no cover
def openapi_generate():
    from pathlib import Path
    import os, re

    base_path = Path(__file__).parent.parent
    messages_path = Path(__file__).parent.joinpath('messages')
    # Generate with protoc tool
    protos_pattern = "open-api-2.0-protobuf-messages/*(Current)*/*.proto"
    protoc_command = "protoc -I=\"%s\" --python_out=%s \"%s\""
    version = ""
    for proto in base_path.glob(protos_pattern):
        command = protoc_command % (
            str(proto.parent.absolute()), str(messages_path), str(proto.absolute()))
        os.system(command)
        if not version: # save the version of current api
            match = re.search("(\d.\d) \(Current\)", str(proto))
            messages_path.joinpath("OpenApiVersion.py").write_text(
                "\n\nversion = \"%s\"" % match.groups())
    # Fix imports
    for pb in messages_path.glob("OpenApi*_pb2.py"):
        content = pb.read_text()
        if re.search("\nimport Open.*", content):
            fix_content = content.replace('import Open', 'from . import Open')
            pb.write_text(fix_content)


@click.command()  # pragma: no cover
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
    template = env.get_template('test_requests.py.j2')
    template.stream(protobufs=protobufs_with_fields).dump("./tests/test_requests.py")


@click.group()  # pragma: no cover
def main():
    pass


main.add_command(openapi_generate)  # pragma: no cover
main.add_command(create_requests)  # pragma: no cover

if __name__ == "__main__":
    from sys import exit
    exit(main())  # pragma: no cover
