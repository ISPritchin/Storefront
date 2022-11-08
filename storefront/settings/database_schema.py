# Settings for getting a graphical representation of the database.
# Use the commands:
# 1. python manage.py graph_models  -a > erd.dot
# 2. python manage.py graph_models  -a -g -o erd.png
import os

os.environ["PATH"] = ''
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True
}