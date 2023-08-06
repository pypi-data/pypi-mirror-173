import typer

app = typer.Typer()


@app.callback()
def callback():
    """

    Awesome Portal GUn
    :return:
    """
    pass


@app.command()
def shoot():
    """
    Shoot the portal gun
    :return:
    """
    typer.echo("shooting portal gun")


@app.command()
def load():
    """
    Shoot the portal gun
    :return:
    """
    typer.echo("loading portal gun")
