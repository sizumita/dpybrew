"""Console script for dpybrew."""
import sys
import urllib.request
import click
import pathlib
from dpybrew import __version__
from .extensions import FileExtension, PyExtension
import yaml
from git import Git
GIST_URL = "https://gist.githubusercontent.com/sizumita/" \
           "19ec79e3ad0ecfae89cca665ddf717e1/raw/b04f8b794ca61cc9701ac8edee37edc52b9f5130/modules.yml"


def error(message):
    click.echo(click.style(message, fg='red'))


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


@main.command(name='install')
@click.argument('names', nargs=-1)
def install_extension(names):
    for name in names:
        click.echo(f'Collectiong {name}')
        target = ""
        if name.startswith("git+"):
            target = name[4:]
        else:
            with urllib.request.urlopen(GIST_URL) as response:
                html = response.read()
            data = yaml.safe_load(html)
            if name in data.keys():
                target = data[name]

        if target == "":
            error(f'  Could not find module "{name}"')
            continue

        Git().clone(target)
        click.echo(f'Successfully installed {name}')


if __name__ == "__main__":
    sys.exit(main())
    # extension_list()
