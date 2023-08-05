from typer import Typer, Option
from PIL import Image

cli = Typer()

@cli.command(hidden=False)
def create(
        size: tuple[int, int] = Option(default=(1080, 1920)),
        color: str = Option(default='#ffffff'),
        filename: str = Option(default='out'),
        category: str = Option(default=''),
        mixed: bool = Option(default=False)
    ):

    img = Image.new('RGB', size, color)
    img.save(f'{filename}.png')
