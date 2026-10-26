"""Deploy only the Blask public file set using explicit, verified FTPS."""
import ftplib
import os
from pathlib import Path
import ssl
import sys
from datetime import datetime, timezone

ROOT = "/domains/blask.korzeniowski.net/public_html"
FILES = (
    "assets/reflective-larch-1706.webp",
    "assets/reflective-larch-1710.webp",
    "assets/reflective-clothing-dim.png",
    "assets/blask-rider-rain-loop-v3.opus",
    "assets/blask-rider-rain-loop-v3.mp3",
    "reflection.js",
    "index.html",
)


def deploy():
    host = os.environ["BLASK_FTP_HOST"]
    port = int(os.environ["BLASK_FTP_PORT"])
    user = os.environ["BLASK_FTP_USERNAME"]
    remote = os.environ["BLASK_FTP_REMOTE_DIR"].rstrip("/")
    if (host, port, user, remote) != (
        "host92093.iqhs.pl", 21, "raf@host92093.iqhs.pl", ROOT
    ):
        raise ValueError("Connection does not match the approved Blask destination")
    site = Path(__file__).resolve().parents[1] / "site"
    if not all((site / name).is_file() and not (site / name).is_symlink() for name in FILES):
        raise ValueError("Public build is incomplete")
    with ftplib.FTP_TLS(context=ssl.create_default_context(), timeout=60) as ftp:
        ftp.connect(host, port)
        ftp.login(user, os.environ["BLASK_FTP_PASSWORD"])
        ftp.prot_p()
        ftp.set_pasv(True)
        ftp.cwd(ROOT)
        if ftp.pwd().rstrip("/") != ROOT:
            raise ValueError("Unexpected FTP working directory")
        existing = set(ftp.nlst())
        if "assets" not in {Path(n).name for n in existing}:
            ftp.mkd("assets")
        # Publish the entry point last so visitors never see incomplete assets.
        for name in FILES:
            target = ".blask-index-upload.html" if name == "index.html" else name
            with (site / name).open("rb") as stream:
                ftp.storbinary("STOR " + target, stream)
            ftp.voidcmd("TYPE I")
            if ftp.size(target) != (site / name).stat().st_size:
                raise ValueError("Uploaded file size mismatch")
            print("Uploaded:", name)
        if "index.html" in {Path(n).name for n in existing}:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            ftp.rename("index.html", f".blask-index-backup-{stamp}.html")
        ftp.rename(".blask-index-upload.html", "index.html")
    print("Blask public site uploaded successfully.")


if __name__ == "__main__":
    try:
        deploy()
    except Exception as error:
        # Do not print exception text, which can contain server or secret values.
        print("Deployment failed:", type(error).__name__, file=sys.stderr)
        sys.exit(1)
