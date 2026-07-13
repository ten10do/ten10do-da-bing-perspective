# 大冰视角 Codex Skill

[![Validate skill](https://github.com/ten10do/ten10do-da-bing-perspective/actions/workflows/validate.yml/badge.svg)](https://github.com/ten10do/ten10do-da-bing-perspective/actions/workflows/validate.yml)

把大冰（焉冰）公开表达中反复出现的思维方式，整理成一个可安装、可核查的 Codex Skill。

它适合用来讨论人生选择、普通人困境、善意行动、内容叙事与长期关系。它不是大冰本人，也不代表本人立场；遇到公开材料未覆盖的新议题时，会明确标注为“模型推断”。

## 能做什么

- 用大冰视角拆解具体问题，而不是只模仿口头禅。
- 用“行动化善意”把善意转成可执行、可验证的方案。
- 用“平行人生加法”分析职业、旅行与生活方式选择。
- 用“普通人行动镜片”和“故事先于教义”改进人物叙事。
- 用“长期关系资产”审视合作、商业与信任成本。

完整能力定义见 [`SKILL.md`](SKILL.md)，框架提炼过程见 [`references/synthesis.md`](references/synthesis.md)。

## 安装

### Windows PowerShell

```powershell
git clone https://github.com/ten10do/ten10do-da-bing-perspective.git "$env:USERPROFILE\.codex\skills\da-bing-perspective"
```

### macOS / Linux

```bash
git clone https://github.com/ten10do/ten10do-da-bing-perspective.git "${CODEX_HOME:-$HOME/.codex}/skills/da-bing-perspective"
```

安装后新建一个 Codex 任务，让 Codex 重新发现 Skill。更新已有安装：

```bash
git -C ~/.codex/skills/da-bing-perspective pull
```

Windows 更新命令：

```powershell
git -C "$env:USERPROFILE\.codex\skills\da-bing-perspective" pull
```

## 使用

显式调用 Skill：

```text
用 $da-bing-perspective 分析：我想辞职旅行，但担心收入中断。
```

也可以使用自然语言触发：

```text
用大冰的视角看看这件事。
如果是大冰，他会怎么劝我？
切换到大冰模式，帮我审视这个公益方案。
按大冰那套，怎么把这个普通人的故事讲好？
```

仅询问大冰的生平、作品或新闻时不会自动触发；普通人生问题若未点名大冰，也不会强行套用该视角。

## 回答方式

Skill 会先判断问题类型，再选择对应模型：

| 问题 | 优先使用 |
| --- | --- |
| 善意、公益、救助 | 行动化善意 |
| 辞职、旅行、多重身份 | 平行人生加法 |
| 人物选择与困境 | 普通人行动镜片 |
| 写作、采访、内容表达 | 故事先于教义 |
| 合作、商业、信任 | 长期关系资产 |

回答通常采用“先接住问题 → 讲清判断 → 给出动作 → 留出边界”的结构。事实型问题会先核查来源；材料未覆盖的新议题会区分公开观点与模型推断。

## 蒸馏依据

- **83 个公开来源**：著作与出版资料、深度访谈、公开表达、外部评价、决策记录和人物时间线。
- **5 个心智模型**：行动化善意、平行人生加法、普通人行动镜片、故事先于教义、长期关系资产。
- **8 条决策启发式**与一套中文表达 DNA。
- **调研截止日期**：2026-07-13。

研究材料按六个维度保存：

1. [`著作与书面材料`](references/research/01-writings.md)
2. [`访谈与长对话`](references/research/02-conversations.md)
3. [`表达 DNA`](references/research/03-expression-dna.md)
4. [`外部评价与批评`](references/research/04-external-views.md)
5. [`关键决策记录`](references/research/05-decisions.md)
6. [`人物时间线`](references/research/06-timeline.md)

## 诚实边界

- 这是基于公开资料构建的思维模型，不是本人授权、数字分身或官方产品。
- 不能保证复现本人的私人判断、现场魅力或对未公开议题的真实态度。
- 不把文学叙事自动当成逐字纪实，也不以传奇个案替代统计证据。
- 医疗、法律、财务和其他高代价问题必须以专业意见与最新事实为准。
- 调研截止日期之后的新作品、直播安排与观点不在当前证据范围内。

## 仓库结构

```text
.
├── SKILL.md                  # 运行时指令与触发规则
├── agents/openai.yaml        # Codex UI 元数据
├── references/synthesis.md   # 心智模型筛选与综合提炼
├── references/research/      # 六个维度的研究与来源
├── scripts/validate_skill.py # 无第三方依赖的结构校验
└── .github/workflows/        # GitHub Actions 自动验证
```

## 验证

```bash
python scripts/validate_skill.py
```

每次推送和 Pull Request 都会运行同一项结构校验。发现来源错误、失效链接或模型越界时，欢迎提交 Issue 或 Pull Request，并附上可核验来源。
