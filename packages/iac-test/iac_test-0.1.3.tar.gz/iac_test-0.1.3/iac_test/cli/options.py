# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Daniel Schmidt <danischm@cisco.com>

import click

data = click.option(
    "-d",
    "--data",
    type=click.Path(exists=True, dir_okay=True, file_okay=True),
    help="Path to data YAML files.",
    required=True,
    multiple=True,
)

templates = click.option(
    "-t",
    "--templates",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="Path to test templates.",
    required=True,
)

filters = click.option(
    "-f",
    "--filters",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="Path to Jinja filters.",
    required=False,
)

tests = click.option(
    "--tests",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="Path to Jinja tests.",
    required=False,
)


output = click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, dir_okay=True, file_okay=False),
    help="Path to output directory.",
    required=True,
)

include = click.option(
    "-i",
    "--include",
    help="Selects the test cases by tag (include).",
    required=False,
    multiple=True,
)

exclude = click.option(
    "-e",
    "--exclude",
    help="Selects the test cases by tag (exclude).",
    required=False,
    multiple=True,
)

render_only = click.option(
    "--render-only",
    is_flag=True,
    help="Only render tests without executing them.",
)
