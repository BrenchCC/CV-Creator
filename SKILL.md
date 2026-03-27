---
name: cv-creator
description: 对话式简历维护技能。开始时先让用户在 Markdown、LaTeX、Markdown + LaTeX 三种模板中选择，再围绕根目录下已有的 resume.md、resume.tex 或两者持续更新。
github_url: https://github.com/Renovamen/oh-my-cv
github_hash: 7543d52f0098c4f908109fdf2b012001a9fb9b6a
version: 0.1.1
created_at: 2026-03-28T00:00:00+08:00
entry_point: scripts/wrapper.py
dependencies: []
---

# CV Creator Skill

这是当前仓库的主技能入口文件。

本技能把 `Renovamen/oh-my-cv` 的 Markdown 驱动思路，与当前仓库里已经存在的 [resume.md](resume.md) 和 [resume.tex](resume.tex) 结合起来，形成一个对话式简历维护流程。

## 核心行为

1. 在任何内容采集前，先让用户从以下 3 个选项里选择一个模板：
   - `Markdown`
   - `LaTeX`
   - `Markdown + LaTeX`
2. 根据用户选择，直接维护根目录下已有的：
   - [resume.md](resume.md)
   - [resume.tex](resume.tex)
   - 或两者
3. 用分步问答收集个人信息、教育、经历、项目、技能等内容。
4. 将用户的原始描述整理成更适合简历表达的结果，尤其是经历和项目部分。
5. 如果用户需要 PDF，优先通过仓库内脚本完成 LaTeX 编译，而不是假设外部路径。

## 什么时候触发

当用户有这些需求时使用本技能：

- 修改当前仓库里的现有简历
- 基于对话逐步完善现有简历
- 同时维护 Markdown 与 LaTeX 两个版本
- 基于已有 PDF / Markdown / LaTeX 提取并重组简历信息
- 需要编译当前仓库的 LaTeX 简历

## 入口规则

第一句必须先问模板选择，不能直接开始问简历内容。

推荐固定问法：

> 开始之前，请先选择你要的简历模板：`Markdown`、`LaTeX`，或 `Markdown + LaTeX`。

如果用户没有明确选择，继续追问这一题，不要跳过。

## 文件职责

- [SKILL.md](SKILL.md)
  当前文件，定义主技能入口、执行规则和文件关系。
- [references/skills.md](references/skills.md)
  主对话流程参考，适用于整个技能。
- [references/auto-cv-reference.md](references/auto-cv-reference.md)
  偏 LaTeX 工作流的历史参考，包含更细的中文简历问答和编译建议。
- [scripts/wrapper.py](scripts/wrapper.py)
  可选工具，用于从结构化 JSON 生成草稿文本；它不是主工作流的真相来源。
- [scripts/install-packages.sh](scripts/install-packages.sh)
  初始化 MiKTeX 宏包，避免编译过程中缺包。
- [scripts/build.sh](scripts/build.sh)
  编译根目录 [resume.tex](resume.tex) 并产出 PDF。

## 推荐执行顺序

1. 读取 [references/skills.md](references/skills.md)。
2. 先问模板选择。
3. 如果用户选择 Markdown：
   - 优先直接更新现有 [resume.md](resume.md)
4. 如果用户选择 LaTeX：
   - 优先直接更新现有 [resume.tex](resume.tex)
5. 如果需要先把结构化内容整理成中间草稿，再决定如何合并：
   - 可选使用 `scripts/wrapper.py render-md --input <json> --output resume.generated.md`
   - 可选使用 `scripts/wrapper.py render-tex --input <json> --output resume.generated.tex`
6. 如果用户需要 PDF：
   - 先确认 `xelatex` 可用
   - 缺包时运行 `bash scripts/install-packages.sh`
   - 编译时运行 `bash scripts/build.sh`

## 设计原则

- 先复用现有文件，再决定是否新增草稿
- 先模板选择，后内容提问
- `resume.md` 和 `resume.tex` 才是主要工作对象
- `wrapper.py` 只是辅助工具，不是主入口
- 所有路径都基于当前仓库，不引用任何旧技能目录路径
