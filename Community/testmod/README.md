# Mod 模板 | Mod Template

将本目录复制到 `Community/` 下并改成你的模组目录名，然后编辑 `mod_descr.ini`、替换 `previews/` 里的示例图。

> 本仓库托管 **模组信息、预览图与下载链接**；不托管模组本体，也不提供青睐与评级服务。

```powershell
Copy-Item -Recurse "Community/mod_template" "Community/HD Terrain Overhaul"
```

MUL 会扫描 `Official/` 与 `Community/` 下的每个目录，读取其中的 `mod_descr.ini`，并按 `[mod] name` 显示模组。目录名建议与模组名一致，便于查找。

---

## 目录结构 | Layout

```
Community/HD Terrain Overhaul/
├── mod_descr.ini     # 必需：唯一的描述文件
└── previews/         # 可选：预览图，1–5 张
    ├── 01.png
    ├── 02.png
    └── 03.png
```

- `previews/` 中可以放 `png` `jpg` `jpeg` `webp` `bmp`，按文件名排序取前 5 张。
- 预览图直接保存在本仓库，不使用外部图床链接。
- 模组本体（zip / 7z 等）不要提交到本仓库，放到下载页中。

---

## mod_descr.ini

```ini
[mod]
name=示例模组
author=你的名字
category=玩法
version=1.0.0
released=2026-11-20
size=12 MB
dlc=false
editor=false
dependencies=Eden ReShade Pack; Mercury Universal Editor

[links]
download=https://pan.baidu.com/s/xxxxxxxx
author=https://space.bilibili.com/xxxxxxx

[summary]
一句话简介，显示在列表卡片上。

[description]
详细介绍，可以写多行。

空行会被保留，MUL 会原样显示在详情页的「详细介绍」区域。
```

### 语法

- `;` 或 `#` 开头的行为注释。
- `[section]` 为分区，`key=value` 为键值。
- `[summary]` 与 `[description]` 之后的所有行会作为文本原样读取，直到下一个 `[分区]`。
- 文件保存为 UTF-8。

### [mod]

| 键 | 必填 | 说明 |
| --- | --- | --- |
| `name` | 是 | 显示名称。 |
| `author` | 是 | 创作者 / 团队，显示在副标题与「作者主页」的默认回退地址中。 |
| `category` | 是 | 只能是 `画面` `材质` `天气` `武器` `界面` `音频` `玩法` `工具`。 |
| `version` | 否 | 版本号，显示为 `v1.0.0`。 |
| `released` | 否 | 发布或更新日期，`YYYY-MM-DD`，用于按日期排序。 |
| `size` | 否 | 安装包大小，例如 `12 MB`。 |
| `dlc` | 否 | `true` / `false`，为真时卡片显示 `DLC` 标签并进入 DLC 筛选。 |
| `editor` | 否 | `true` / `false`，编辑器类组件标记。 |
| `dependencies` | 否 | 依赖的模组名称，用 `;` 或 `,` 分隔；MUL 会在详情页逐条检查是否已安装。 |

### [links]

只允许两个自定义跳转页面：

| 键 | 说明 | 留空时 |
| --- | --- | --- |
| `download` | 下载页，可指向百度云、OneDrive、GitHub Releases 等 | 回退到模组 GitHub 仓库的 Releases |
| `author` | 作者主页，可指向 B 站、个人博客、GitHub 主页等 | 回退到 `https://github.com/<author>` |

### 预览图

- 放在 `previews/` 下，1–5 张，建议 16:9。
- MUL 详情页显示缩略图；**点击缩略图会从仓库读取并显示原图**，不会缩放压缩。
- 未提供预览图的模组会显示占位图。

### 不写入 ini 的内容

以下由 MUL 本地或社区统计维护，**不要**写进 `mod_descr.ini`：

- `installed` / `updatable`：本地安装状态。
- 青睐、评级：用户本机操作，仓库不提供这两个服务。
- 爱心、社区青睐：社区统计。

---

## 提交检查清单 | Checklist

- [ ] 目录内存在 `mod_descr.ini`，UTF-8 编码，无占位符残留。
- [ ] `name`、`author`、`category` 已填写，`category` 属于 8 个分类之一。
- [ ] `[summary]` 与 `[description]` 内容完整。
- [ ] `previews/` 中 1–5 张图片，文件名有序。
- [ ] `[links]` 最多两个链接，且不指向本仓库内的文件。
- [ ] 模组本体未提交到本仓库，且分发方式符合 MFL。
