# 维护备忘

给作者本人用的操作记录：发布、换电脑、脚本用法。日常访客不用看。

## 发布到 GitHub Pages

现已发布：<https://chengyi-mountain.github.io/buyi/>

改动推上 `main` 后会自动重新部署，通常一两分钟生效。若需重新开启：

1. 仓库根目录保留 `index.html`（Pages 默认首页）。
2. Settings → Pages → Source 选 `main` / `(root)` → Save。
3. 等一两分钟后打开 <https://chengyi-mountain.github.io/buyi/>。

## 换电脑 / 继续修改

GitHub 上的仓库是唯一权威副本，本地那份只是工作副本。原电脑重装、换机器、文件误删，都不影响已经推上去的版本。

- **新电脑继续改**：装 GitHub Desktop → 菜单 `File` → `Clone repository` → 选 `chengyi-mountain/buyi` → 指定本地目录 → Clone。拿到的是带完整提交历史的可编辑副本。
- **别用网页 Download ZIP**：只有文件、没有历史，改完再推容易和远端分叉。
- **改完推送**：GitHub Desktop 里 `Commit to main` → 右上 `Push origin`。
- **两边都改过**：先点 `Fetch origin`，再 `Pull`，处理完冲突再推。
- **不要在网页上直接上传同名文件改内容**：会和本地副本分叉，下次 Push 报 “Newer commits on remote”。

## 脚本用法

均需在仓库根目录执行，Python 3。

| 脚本 | 用途 | 命令 |
| --- | --- | --- |
| `tools/fetch_text.py` | 重抓《周易》经文到 `data/64gua.json` | `python tools/fetch_text.py` |
| `tools/build.py` | 合并 `64gua.json` + `notes_*.json`，整段替换 `index.html` 里的 `const YI` | `python tools/build.py` |
| `tools/split_book.py` | 把讲义 PDF 拆成 `001.jpg`～`064.jpg` | `python tools/split_book.py <pdf> assets/renjiandao --mode full --dpi 150` |
| `tools/inspect_pdf.py` | 检查 PDF 页数、每页图片对象 | `python tools/inspect_pdf.py <pdf>` |
| `tools/make_manifest.py` | 重算内容哈希清单 `NOTICE.sha256` | `python tools/make_manifest.py` |

拆页说明：`--mode full` 导整页（含卦名与「卦圖象解」），`--mode crop` 只裁画作区，但各页画幅不一致时会切坏，默认用 `full`。

## 版本与校验

- 校验当前版本是否被改动：`python tools/make_manifest.py` 重新生成 `NOTICE.sha256`，与已存清单逐行比对哈希。
- 每次大改后可打标签留节点：`git tag -a v0.2.0 -m "说明"`，再 `git push origin v0.2.0`。
