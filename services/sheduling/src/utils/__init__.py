from pathlib import Path
import os

ROOT_FLD = Path(__file__).parent.parent.parent.parent.parent.as_posix()
TMP_FLD = os.path.join(ROOT_FLD, 'tmp')