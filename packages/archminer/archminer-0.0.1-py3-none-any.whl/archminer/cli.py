# SPDX-FileCopyrightText: 2022-present Ben Companjen <ben@companjen.name>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import click
import pdfminer

@click.command()
@click.option('out-file', type=click.Path())
@click.argument('in-file', type=click.Path())
def main(in_file, out_file):
    """Mine the PDF!"""
    click.echo(in_file)
    click.echo(out_file)
