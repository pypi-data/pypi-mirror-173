# ------------------------------------------------------------------------------
#  leonard [Configurable fast-access toolset]
#  (C) 2022. A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------



@click.group(cls=CliGroup)
@click.version_option(APP_VERSION, "-V", "--version")
@click.pass_context
def es7s(ctx: click.Context, **kwargs):
    """
    Entrypoint of es7s system CLI.
    """
    pass



entrypoint = leonard


def extcall():
    entrypoint()
