import traceback

import panel as pn
from unimport.analyzers import MainAnalyzer
from unimport.refactor import refactor_string
from unimport.statement import Import


def refactor(source: str) -> str:
    with MainAnalyzer(source=source, include_star_import=True):
        unused_imports = list(Import.get_unused_imports(include_star_import=True))

    return refactor_string(source=source, unused_imports=unused_imports)


def run_refactor(source: str) -> pn.widgets.Ace:
    try:
        refactored_source = refactor(source)
        language = "python"
    except Exception:
        refactored_source = traceback.format_exc()
        language = "text"

    return pn.widgets.Ace(
        value=refactored_source,
        language=language,
        readonly=True,
    )


pn.config.sizing_mode = "stretch_both"
pn.extension()


example_source_code = """\
import x


"""

source_editor = pn.widgets.Ace(value=example_source_code, language="python")
result_editor = pn.bind(run_refactor, source_editor)


docs_button = pn.widgets.Button(name="Go to docs", button_type="primary", width=100)
docs_button.js_on_click(code="window.open('https://unimport.hakancelik.dev')")
github_button = pn.widgets.Button(name="GitHub", button_type="primary", width=100)
github_button.js_on_click(code="window.open('https://github.com/hakancelikdev/unimport')")

app_row = pn.Row(source_editor, result_editor)

bootstrap = pn.template.MaterialTemplate(title="Try Unimport")
bootstrap.header.append(pn.Row(docs_button, github_button))
bootstrap.main.append(app_row)
bootstrap.servable()
