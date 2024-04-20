import gfpgan
import basicsr

try:
    print("GFPGAN version:", gfpgan.__version__)
except AttributeError:
    print("GFPGAN version not available")

try:
    print("BasicSR version:", basicsr.__version__)
except AttributeError:
    print("BasicSR version not available")
