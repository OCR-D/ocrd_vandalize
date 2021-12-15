from json import loads
from pkg_resources import resource_string, resource_filename

OCRD_TOOL = loads(resource_string(__name__, 'ocrd-tool.json'))
FONT = resource_filename(__name__, 'UnifrakturMaguntia.ttf')
