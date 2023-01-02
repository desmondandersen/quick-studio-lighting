# Quick Studio Lighting

Add this library to your scripts directory. Then run this in the Maya script editor.

```python
import importlib
import sys

sys.path.append("...") # Path to your scripts directory path

from quickStudio import studioLighting
importlib.reload(studioLighting)


studioLighting.show_ui()
```