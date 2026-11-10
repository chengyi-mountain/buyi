# 操作手册

不用 AI 也能自己维护这个站：从零建仓库、日常改一处、到最后发布。全部是点鼠标和敲一两行命令，没有玄的东西。

---

## 一、先把三件事记住

1. **GitHub 上的仓库是唯一正本**，你电脑里那份只是工作台。工作台坏了没关系，Clone 回来即可。
2. **页面只有一个文件**：`index.html`（样式、脚本、六十四卦数据全在里面）。改它就是改站。
3. **两个动作能让改动上线**：`Commit to main` → `Push origin`。少一步，线上不变。

---

## 二、从零建一个同样的项目（复盘一次就会）

### 1. 装两样东西
- **Python 3**：安装时勾上 `Add Python to PATH`，装完在 PowerShell 里敲 `python --version`，能出版本号就成。
- **GitHub Desktop**：登录自己的 GitHub 账号。

### 2. 建仓库
打开 GitHub Desktop → 菜单 `File` → `New repository` → 选 `Create new repository`：
- `Name` 填 `buyi`
- `Local path` 填**上一级目录**，比如 `C:\Users\你的名字\Desktop\GitHub`
- 其余默认 → `Create repository`

建完本地会出现 `…\Desktop\GitHub\buyi` 这个空文件夹，把项目文件放进去。

### 3. 首次发布
回到 GitHub Desktop，顶部按钮写的是 **Publish repository**（不是 Push）：
- 点它 → 弹窗里**取消勾选** `Keep this code private` → 发布。

只有第一次是 Publish。之后同一个仓库都显示 `Push origin`。

### 4. 开网页
浏览器打开自己仓库 → 页面上方 `Settings` → 左侧 `Pages` → `Source` 选 `main` 和 `/(root)` → `Save`。等一两分钟，地址固定为：

```
https://你的用户名.github.io/buyi/
```

---

## 三、日常改一处：固定五步

1. **改文件**（下面第四节按改什么分类）。
2. **本地看效果**：双击 `index.html`，浏览器里翻一遍。改完没变化，按 `Ctrl + Shift + R` 强制刷新。
3. **跑脚本**（只在改数据时才需要，见第四节）。
4. **提交**：GitHub Desktop 左栏是改动文件列表，左下 `Summary` 写一句人话，比如「换第 3 卦人间道文字」，点 `Commit to main`。
5. **推送**：点右上 `Push origin`。等一两分钟刷线上地址确认。

改了没看到效果，先查这三点：本地文件存没存、Commit 有没有做、Push 有没有点。

---

## 四、三类改动，各自怎么弄

### A. 改文字（三栏意解、文案）
- 三栏文字在 `data/notes_01.json` ～ `notes_09.json`，按卦号排列，每卦三个字段：
  `r` 人间道、`z` 阳宅学、`c` 案例。
- 用记事本或 VS Code 打开，找到 `"n": 3` 那一段，改引号里的内容。
- **别动结构**：字段名、冒号、逗号、双引号都要留着。中文不要用英文引号包中文以外的符号。
- 改完执行：`python tools/build.py`。它会把这些文字重新灌进 `index.html`。
- 页面上的纯文案（按钮字、提示语、页脚）直接在 `index.html` 里搜索那句话改。

### B. 加图 / 换图
- 图放 `assets/renjiandao/`，命名必须 `001.jpg`（乾卦）到 `064.jpg`（未济），三位数、小写 `.jpg`。
- 直接覆盖同名文件即可，**不用跑脚本**，刷新页面就换。
- 有 PDF 想批量拆页：`python tools/split_book.py <pdf路径> assets/renjiandao --mode full --dpi 150`
  （`--mode crop` 只裁画作区，各页画幅不一致时会切坏，用 `full`。）

### C. 改样式 / 改交互
- 都在 `index.html` 里。样式在 `<style>` 段，脚本在 `<script>` 段，六十四卦数据在 `const YI = [...]`。
- **改前先复制一份**当退路：同一目录下存成 `index-备份日期.html`。它是备份，不用提交（GitHub Desktop 会看到它，别勾）。
- 想改颜色：搜 `:root` 那一块，里面是全局色值，改一处全站跟着变。
- 想改宽度、间距：搜对应的 `class` 名。

---

## 五、版权与署名怎么维护

已经是分层的，别推翻重来，只按下面更新：

| 什么时候 | 改哪里 |
| --- | --- |
| 页面加了新内容 / 改了作者名 | `index.html` 页脚那一行 `© 年份 chengyi-mountain` |
| 权利归属变了（比如换了图源） | `NOTICE.md` 对应那一条，并在 README 的「版权与署名」表里同步 |
| 每次正式改动后 | 跑 `python tools/make_manifest.py`，更新 `NOTICE.sha256`（内容哈希清单，用来证明某版本内容没被改过） |
| 大版本定稿 | `git tag -a v0.2.0 -m "说明"`，再推一次 tag |

三条底线别越：
- 不要把整站说成「完全原创」——图解是他人扫描件，经文是公有领域，只有页面、脚本、三栏文字是你的。
- 不要加 MIT / Apache 这类开源许可，那等于授权别人随便用。
- 图解不要用于任何收费场景，也不要二次转发到别的平台。

## 六、项目介绍（README）怎么写

结构固定成六块，读者三秒能看懂：

1. **一句话定位**：这是什么、给谁看。
2. **在线地址**：能点开就先用。
3. **怎么用**：五个视图一张表，按钮一句话。
4. **目录**：三五行，说清哪个文件管什么。
5. **改内容**：三步，写给未来的自己。
6. **版权与署名 + 声明**：表格 + 几条禁忌。

写法上守两条：先讲「是什么」再讲「怎么改」；部署、换电脑这类操作别塞进来，放 `MAINTENANCE.md`。

---

## 七、出事怎么办

| 现象 | 处理 |
| --- | --- |
| 线上没变化 | 先确认 Push 点了；再看仓库 `Actions` 里部署是否跑完；等两分钟；`Ctrl + Shift + R` |
| 图片显示不出来 | 检查文件名是否三位数、是否小写 `.jpg`、是否放对目录 |
| 页面白屏或按钮死了 | 多半是 `index.html` 里改坏了结构：把备份文件覆盖回去 |
| Push 报 “Newer commits on remote” | 先 `Fetch origin` 再 `Pull`，再 Push |
| 改完想撤回 | GitHub Desktop 的 `History` 里右键那次提交 → `Revert commit` |
| 本地文件全丢了 | GitHub Desktop → `File` → `Clone repository` → 选自己的仓库，重新拉下来 |

---

## 八、命令速查

在仓库目录下打开 PowerShell（在文件夹空白处按住 `Shift` 右键 → `在此处打开 PowerShell`）：

```
python tools\build.py            # 改完 notes_*.json 后，把文字灌进页面
python tools\fetch_text.py       # 重抓《周易》经文
python tools\make_manifest.py    # 重算 NOTICE.sha256
python tools\shrink_images.py 800   # 把图解缩到 800px 宽，原图自动备份到 buyi-原图备份
python tools\inspect_pdf.py 某.pdf   # 看 PDF 有多少页、每页几张图
python tools\split_book.py 某.pdf assets\renjiandao --mode full --dpi 150
```
