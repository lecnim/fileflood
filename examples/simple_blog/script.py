from os.path import dirname
from rucola import Rucola

# Used plugins:
from rucola_markdown import Markdown
from rucola_yamlfm import YamlFrontmatter
from rucola_mustache import MustacheLayouts
from rucola_permalinks import Permalinks
from rucola_collections import Collections

# Set working directory relative to location of this file
app = Rucola(dirname(__file__))
# Remove previous build directory
app.clear_output()

app.use(
    YamlFrontmatter(),
    Collections(),
    Markdown(),
    MustacheLayouts(),
    Permalinks()
)

app.build()
