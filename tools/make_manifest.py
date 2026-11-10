# -*- coding: utf-8 -*-
"""生成仓库内容的 SHA-256 清单（NOTICE.sha256），用于证明某时刻版本内容。

用法：python tools/make_manifest.py
输出：仓库根目录 NOTICE.sha256，含生成时间、git 提交号与各文件哈希。
"""
import hashlib
import io
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "NOTICE.sha256")


def _git_exe():
    """优先用 PATH 里的 git，否则用 GitHub Desktop 自带的 git。"""
    import glob
    cand = glob.glob(os.path.expandvars(
        r"%LOCALAPPDATA%\GitHubDesktop\app-*\resources\app\git\cmd\git.exe"))
    if cand:
        return sorted(cand)[-1]
    return "git"


def git(*args):
    try:
        out = subprocess.run([_git_exe(), "-C", REPO, *args], capture_output=True, text=True)
        return out.stdout.strip()
    except FileNotFoundError:
        return ""


def tracked_files():
    names = git("ls-files")
    if names:
        return [n for n in names.splitlines() if n]
    # 无 git 可用时退回逐目录遍历
    result = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            p = os.path.join(root, f)
            result.append(os.path.relpath(p, REPO).replace("\\", "/"))
    return sorted(result)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    files = [f for f in tracked_files() if f != "NOTICE.sha256"]
    if not files:
        print("no files found", file=sys.stderr)
        return 1
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S +0800")
    head = git("rev-parse", "HEAD") or "(not a git repo)"
    lines = []
    lines.append("卜易 · buyi　内容清单（SHA-256）")
    lines.append("项目：https://github.com/chengyi-mountain/buyi")
    lines.append("生成时间：" + now)
    lines.append("对应提交：" + head)
    lines.append("文件数：" + str(len(files)))
    lines.append("")
    lines.append("校验方法：sha256sum -c NOTICE.sha256（Linux/macOS）；")
    lines.append("          Get-FileHash <文件> -Algorithm SHA256（Windows）")
    lines.append("")
    for name in files:
        path = os.path.join(REPO, name.replace("/", os.sep))
        if not os.path.exists(path):
            lines.append("%-46s  (missing)" % name)
            continue
        lines.append("%s  %s" % (sha256(path), name))
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("written:", OUT, "files:", len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
