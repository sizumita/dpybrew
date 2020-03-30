"""Console script for dpybrew."""
import sys
import os
import click
import pathlib
from dpybrew import __version__
from .extensions import FileExtension, PyExtension


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'dpybrew {__version__}')
    ctx.exit()


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.pass_context
def main(ctx, args=None):
    """Console script for dpybrew."""
    if ctx.invoked_subcommand:
        return
    click.echo(f'dpybrew {__version__}')
    return 0


@main.command(name='list')
@click.argument('filepath', nargs=1, default='.')
def extension_list(filepath):
    """Show list of extensions."""
    path = pathlib.Path.cwd()/pathlib.Path(filepath)
    file_extensions = [FileExtension(p.relative_to(p.cwd())) for p in path.iterdir()
                       if p.is_dir() and not p.name.startswith(('.',  '__'))]
    py_extensions = [PyExtension(p.relative_to(p.cwd())) for p in path.glob('*.py') if not p.name.startswith(('.',  '__'))]
    extensions = sorted(file_extensions + py_extensions, key=lambda x: str(x))

    for extension in extensions:
        if extension.has_setup():
            if version := extension.get_version() is not None:
                text = f'{extension} {version}'
            else:
                text = str(extension)
            click.echo(click.style(text, fg='yellow', bold=True))
        else:
            click.echo(click.style(str(extension), fg='blue'))


if __name__ == "__main__":
    sys.exit(main())
    # extension_list()
