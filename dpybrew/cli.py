"""Console script for dpybrew."""
import sys
import click
from dpybrew import __version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'dpybrew {__version__}')
    ctx.exit()


@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def main(args=None):
    """Console script for dpybrew."""
    click.echo(f'dpybrew {__version__}')
    return 0


@click.command(name='list')
@click.argument('filepath', nargs=1, default='.')
def extension_list(filepath):
    """Show list of extensions."""
    print(sys.path)


if __name__ == "__main__":
    sys.exit(main())

