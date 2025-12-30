# src/fw/logger.py
import logging
from pathlib import Path

def setup_logger(level: str = "INFO", file_path: str = "logs/test.log") -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # pytest tekrar çağırırsa handler şişmesin
    for h in list(root.handlers):
        root.removeHandler(h)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")

    fh = logging.FileHandler(file_path, encoding="utf-8")
    fh.setFormatter(fmt)

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)

    root.addHandler(fh)
    root.addHandler(sh)

    # İsteğe bağlı gürültü azaltma
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
