import sys, random
from pathlib import Path

def bootstrap(seed=1):
    # seeds
    random.seed(seed)
    try:
        import numpy as np; np.random.seed(seed)
    except ImportError:
        pass
    try:
        import torch; torch.manual_seed(seed)
    except ImportError:
        pass

    # project root (one level up from /notebooks)
    root = Path().resolve().parents[0]

    # make src importable
    sys.path.append(str(root / "src"))

    # ensure standard folders
    data   = (root / "data");   data.mkdir(parents=True, exist_ok=True)
    figs   = (root / "figs");   figs.mkdir(parents=True, exist_ok=True)
    models = (root / "models"); models.mkdir(parents=True, exist_ok=True)
    logs   = (root / "logs");   logs.mkdir(parents=True, exist_ok=True)

    return root, data, figs, models, logs
