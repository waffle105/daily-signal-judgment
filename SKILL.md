---
name: daily-signal-judgment
description: 生成“每日核心信号”和“今日一句话判断”中文图文内容，包括手写纸张风格竖版信息图、小红书式详情文案、来源与话题，并按北京时间以 YYMMDD 六位日期文件夹归档。适用于用户要求制作每日 AI/产业/组织趋势信号、一句话判断、同款栏目图、配套详情文字，或把成品图片和文案保存到对应主文件夹的任务。
---

# 每日核心信号与一句话判断

把同一主题提炼为两个互补栏目：

- “每日核心信号”：回答“正在发生什么结构性变化”。
- “今日一句话判断”：回答“因此今天应该如何判断或行动”。

## 工作流

1. 确认输出范围：生成两个栏目，除非用户只点名其中一个。
2. 确定当天主题与证据：
   - 优先使用用户提供的材料、链接或观点。
   - 若用户只说“生成今天的”，浏览最近 24–72 小时的一手或权威来源；不得编造新闻、数据或出处。
   - 观点性内容可标注“来源：一宏的碎碎念，仅供参考”；事实性内容必须写真实来源名称。
3. 读取 [references/content-and-visual-spec.md](references/content-and-visual-spec.md)，完成两套标题、图中文字、画面结构和详情文案。
4. 先写详情文案，再从文案中压缩图片文字，确保两者口径一致。
5. 使用内置 `image_gen`，每个栏目单独生成一张竖版图片。把 `assets/` 中对应参考图的左侧成图区域作为风格与版式参考，不作为需要修改的目标图；忽略截图右侧的平台界面。
6. 检查生成图：日期、栏目名、主标题、流程词、汉字可读性和无水印。若关键文字错误，做一次只修文字的定向迭代；仍有错误时明确告知，不把错图当最终稿。
7. 用归档脚本建立目录并保存：

```powershell
python "<本 Skill 目录>\scripts\archive_daily.py" --root "<当前项目主目录>" --series both
```

生成单个栏目后，将图片和 UTF-8 文案文件归档：

```powershell
python "<本 Skill 目录>\scripts\archive_daily.py" --root "<当前项目主目录>" --series core-signal --image "<生成图路径>" --content-file "<临时文案路径>"
python "<本 Skill 目录>\scripts\archive_daily.py" --root "<当前项目主目录>" --series one-line-judgment --image "<生成图路径>" --content-file "<临时文案路径>"
```

8. 最终回复中列出两个日期文件夹、图片与文案的绝对路径，并简述选用的当天主题。

## 归档约定

以 Asia/Shanghai 当地日期生成六位 `YYMMDD`，例如 2026-07-25 为 `260725`：

```text
<当前项目主目录>/
├─ 每日核心信号/
│  └─ 260725/
│     ├─ cover.png
│     └─ content.txt
└─ 今日一句话判断/
   └─ 260725/
      ├─ cover.png
      └─ content.txt
```

不要把最终图片只留在 `.codex/generated_images`。归档脚本不会覆盖已有文件；重复生成时自动保存为 `cover-v2.png`、`content-v2.txt` 等。

## 内容要求

- 两张图围绕同一主题，但不得只是换标题复述。
- 核心信号偏“趋势解释”，一句话判断偏“决策结论”。
- 主标题要具体、可争辩、可复述，避免“AI 很重要”一类空话。
- 详情文案自然分段，不使用表格，不写虚假数据，不夸大确定性。
- 每篇末尾保留 4–6 个高相关话题；需要搜索词时再加一行“猜你想搜：……”。
- 图片中的来源短句与详情文案来源保持一致。

## 参考资源

- `assets/core-signal-reference.png`：每日核心信号视觉参考；只参考左侧成图。
- `assets/judgment-reference.png`：今日一句话判断视觉参考；只参考左侧成图。
- `assets/core-signal-caption-reference.png`：核心信号详情文案结构参考。
- `assets/judgment-caption-reference.png`：一句话判断详情文案结构参考。
- `references/content-and-visual-spec.md`：写作模板、画面规范与生成提示词骨架。
- `scripts/archive_daily.py`：建立日期目录并无覆盖归档。
