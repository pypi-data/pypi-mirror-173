from importlib import import_module

import typer

from .converters.jinja import JinjaConverter  # type: ignore
from .converters.markdown import MarkdownConverter  # type: ignore

app = typer.Typer()


@app.command()
def main(model_path, format: str = typer.Option("hcl")):
    module_path, class_name = model_path.split(":", 2)
    module = import_module(module_path)
    model = getattr(module, class_name)

    if format == "markdown":
        converter = MarkdownConverter(format=format)
    else:
        converter = JinjaConverter(format=format)

    print(converter.convert(model))


if __name__ == "__main__":
    app()
