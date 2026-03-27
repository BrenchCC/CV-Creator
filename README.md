# cv-creator

`cv-creator` 是一个围绕现有简历文件做维护的仓库。

它的核心不是重新生成模板，而是通过对话式流程，持续更新当前仓库里的：

- `resume.md`
- `resume.tex`

用户开始时需要先选择 3 个模板选项之一：

1. `Markdown`
2. `LaTeX`
3. `Markdown + LaTeX`

随后流程会根据选择，更新对应文件。

## 仓库结构

- `resume.md`
  当前 Markdown 简历源稿。
- `resume.tex`
  当前 LaTeX 简历源稿。
- `SKILL.md`
  主技能入口说明。
- `references/skills.md`
  主对话流程参考。
- `references/auto-cv-reference.md`
  偏 LaTeX 工作流的补充参考。
- `scripts/build.sh`
  编译 `resume.tex` 并生成 PDF。
- `scripts/install-packages.sh`
  初始化 MiKTeX 宏包。
- `scripts/wrapper.py`
  可选辅助工具，用于从结构化 JSON 生成草稿内容。

## 工作方式

推荐顺序：

1. 先确定使用 `Markdown`、`LaTeX`，还是 `Markdown + LaTeX`
2. 直接修改现有 `resume.md`、`resume.tex` 或两者
3. 只有在需要中间草稿时，才使用 `scripts/wrapper.py`
4. 如果需要 PDF，再运行编译脚本

## 脚本用法

初始化 LaTeX 编译依赖：

```bash
bash scripts/install-packages.sh
```

编译 PDF：

```bash
bash scripts/build.sh
```

从结构化 JSON 生成 Markdown 草稿：

```bash
python scripts/wrapper.py render-md --input data.json --output resume.generated.md
```

从结构化 JSON 生成 LaTeX 草稿：

```bash
python scripts/wrapper.py render-tex --input data.json --output resume.generated.tex
```

## 说明

- `resume.md` 和 `resume.tex` 是主要工作对象
- `wrapper.py` 只是辅助工具，不是主入口
- 如果只维护 LaTeX，可以完全不使用 `wrapper.py`
