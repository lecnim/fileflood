import os
from rucola import Rucola
from rucola_markdown import Markdown
from rucola_yamlfm import YamlFrontmatter
from rucola_mustache import MustacheLayouts
from rucola_permalinks import Permalinks

app = Rucola(os.path.dirname(__file__))
app.clear_output()

app.use(
    YamlFrontmatter(),
    Markdown(),
    MustacheLayouts(),
    Permalinks()
)

app.build()