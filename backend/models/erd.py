# Generate ERD diagram

from eralchemy import render_er
from ..main import masterconfig

render_er(masterconfig['db'], 'erd.png')