# 常微分方程 · 点化学习系统

七本常微分方程教材/辅导书整合成的一套可直接开学的知识库。总入口是 `index.html`（单文件，离线可开）。

## 打开方式

直接双击 `index.html`。不需要服务器，不需要联网。

打开后：
- 顶部切换「跨书总览」与七本书；
- 左侧是本册导航：学习路径 / 各章精讲 / 概念页 / 测验 / 抽认卡 / 术语 / 模式库 / 速查表；
- 右上角搜索框覆盖全部书；
- 阅读进度按书独立保存在浏览器里（清缓存会丢）。

每本书还带一个单书伴侣 `NN-书名/<slug>学习伴侣.html`，内容同源，可以单独发给同学。

## 目录结构

```
常微分方程点化学习系统/
├── index.html              # 总学习手册（单文件入口）
├── index.md                # Markdown 导航
├── README.md               # 本文件
├── .nojekyll               # GitHub Pages 关闭 Jekyll
├── 交付说明.md             # 交付清单、验证结论、取舍
├── 00-跨书总览/            # 推荐顺序 / 概念映射 / 综合检验
├── 01-王高雄-常微分方程/    # 主干教材（8 章）
├── 02-朱思铭-学习辅导与习题解答/  # 解题辅导（8 章）
├── 03-习题详解-第四版/     # 配套习题（8 章）
├── 04-柳彬-常微分方程/     # 理论版（9 章）
├── 05-丁同仁-常微分方程教程/ # 最完整理论版（11 章）
├── 06-庞特里亚金-常微分方程/ # 数学与工程（6 章）
├── 07-阿诺尔德-常微分方程/  # 几何视角（7 个学习单元）
└── _build/                 # 目录 OCR、组装脚本、验证报告
```

每本书目录内统一为：`SKILL.md`（总纲）、`chapters/`、`concepts/`、`glossary.md`、`patterns.md`、`cheatsheet.md`、`quiz.md`、`flashcards.md`、`manifest.json`、`<slug>学习伴侣.html`。

## 部署到 GitHub Pages

```bash
# 1. 解压到仓库根目录
unzip 常微分方程点化学习系统.zip -d my-ode-site
cd my-ode-site/常微分方程点化学习系统

# 2. 推上去
git init && git add -A && git commit -m "ODE handbook"
git remote add origin https://github.com/<你的账号>/<仓库名>.git
git push -u origin main

# 3. 仓库 Settings → Pages → Source 选 Deploy from a branch → main / (root) → Save
```

两三分钟后访问 `https://<你的账号>.github.io/<仓库名>/`。

`index.html` 是单文件，所以根目录直接指向它就行，不需要额外配置。`.nojekyll` 已放在根目录，避免 Jekyll 吞掉中文目录名和 `_build/`。

**注意**：`index.html` 内嵌了全部内容，体积约 785 KB，首次加载在移动网络下会有几秒白屏，属正常。

## 已知限制

- 数学公式用纯文本记号（`e^(At)`、`xᵀPx`、`∫`）书写，不用 LaTeX 渲染。原因是本机与外网均无 KaTeX 可用，硬接 CDN 在离线/内网环境下会显示成源码，不如统一用可读的文本记号。
- Mermaid 图联网时自动渲染，离线时显示源码并给出提示。图的正文说明都写在图下方，不依赖渲染也能读。
- 五本原书是纯扫描件（王高雄、朱思铭、丁同仁、庞特里亚金、阿诺尔德），章节结构由目录页 OCR 与逐页读图核对，公式按标准教材口径重写，不与扫描件逐字对应。

## 修订

改任意一册的内容后：

```bash
python3 _build/make_book.py <slug>          # 重生成 quiz/flashcards/manifest
python3 .../build_companion.py --manifest <书目录>/manifest.json --out <书目录>/<slug>学习伴侣.html
python3 .../build_handbook.py --root . --order "01,02,03,04,05,06,07"
python3 .../verify_handbook.py --index index.html --chromium /usr/local/bin/chromium
```
