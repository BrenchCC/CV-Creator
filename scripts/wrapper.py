import argparse
import json
from pathlib import Path


MARKDOWN_TEMPLATE = """# {name}

{role_or_title}

- {city}
- {email}
- {phone}
- {website}
- {github}
- {linkedin}

## Summary

- {summary_1}
- {summary_2}
- {summary_3}

## Education

### {school_1}
{degree_1} in {major_1} · {education_time_1}

- {education_note_1}

## Experience

### {company_1} · {title_1}
{experience_time_1} · {team_1}

{scope_1}

- {experience_bullet_1}
- {experience_bullet_2}
- {experience_bullet_3}

## Projects

### {project_1} · {project_role_1}
{project_time_1}

Tech Stack: {project_stack_1}

{project_scope_1}

- {project_bullet_1}
- {project_bullet_2}
- {project_bullet_3}

## Skills

- Languages: {languages}
- Frameworks: {frameworks}
- Tools: {tools}
- Platforms: {platforms}
"""

LATEX_TEMPLATE = r"""\documentclass[11pt,a4paper]{{article}}
\usepackage[margin=0.7in]{{geometry}}
\usepackage{{enumitem}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{titlesec}}
\usepackage{{parskip}}

\setlist[itemize]{{leftmargin=1.2em, topsep=2pt, itemsep=2pt}}
\titlespacing*{{\section}}{{0pt}}{{8pt}}{{4pt}}
\titleformat{{\section}}{{\large\bfseries}}{{}}{{0em}}{{}}[\titlerule]
\pagestyle{{empty}}

\begin{{document}}

\begin{{center}}
    {{\LARGE \textbf{{{name}}}}}\\
    {role_or_title}\\
    {city} \quad {email} \quad {phone} \quad {website}
\end{{center}}

\section*{{Summary}}
\begin{{itemize}}
    \item {summary_1}
    \item {summary_2}
    \item {summary_3}
\end{{itemize}}

\section*{{Education}}
\textbf{{{school_1}}} \hfill {education_time_1}\\
{degree_1} in {major_1}\\
{education_note_1}

\section*{{Experience}}
\textbf{{{company_1}}} --- {title_1} \hfill {experience_time_1}\\
{team_1}\\
{scope_1}
\begin{{itemize}}
    \item {experience_bullet_1}
    \item {experience_bullet_2}
    \item {experience_bullet_3}
\end{{itemize}}

\section*{{Projects}}
\textbf{{{project_1}}} --- {project_role_1} \hfill {project_time_1}\\
Tech Stack: {project_stack_1}\\
{project_scope_1}
\begin{{itemize}}
    \item {project_bullet_1}
    \item {project_bullet_2}
    \item {project_bullet_3}
\end{{itemize}}

\section*{{Skills}}
\textbf{{Languages}}: {languages}\\
\textbf{{Frameworks}}: {frameworks}\\
\textbf{{Tools}}: {tools}\\
\textbf{{Platforms}}: {platforms}

\end{{document}}
"""


def parse_args():
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        description = "Render draft Markdown or LaTeX CV content from structured JSON."
    )
    subparsers = parser.add_subparsers(
        dest = "command",
        required = True
    )

    init_md_parser = subparsers.add_parser(
        "init-md",
        help = "Create a draft markdown resume skeleton."
    )
    init_md_parser.add_argument(
        "--output",
        required = True,
        help = "Output markdown path."
    )
    init_md_parser.add_argument(
        "--force",
        action = "store_true",
        help = "Overwrite the target file if it exists."
    )

    render_md_parser = subparsers.add_parser(
        "render-md",
        help = "Render a draft markdown resume from JSON data."
    )
    render_md_parser.add_argument(
        "--input",
        required = True,
        help = "Input JSON path."
    )
    render_md_parser.add_argument(
        "--output",
        required = True,
        help = "Output markdown path."
    )
    render_md_parser.add_argument(
        "--force",
        action = "store_true",
        help = "Overwrite the target file if it exists."
    )

    render_tex_parser = subparsers.add_parser(
        "render-tex",
        help = "Render a draft LaTeX resume from JSON data."
    )
    render_tex_parser.add_argument(
        "--input",
        required = True,
        help = "Input JSON path."
    )
    render_tex_parser.add_argument(
        "--output",
        required = True,
        help = "Output tex path."
    )
    render_tex_parser.add_argument(
        "--force",
        action = "store_true",
        help = "Overwrite the target file if it exists."
    )

    return parser.parse_args()


def ensure_parent_dir(output_path):
    """Create the parent directory for an output path.

    Args:
        output_path: Target file path.
    """

    output_path.parent.mkdir(
        parents = True,
        exist_ok = True
    )


def write_text(
    output_path,
    content,
    force = False
):
    """Write text content to disk.

    Args:
        output_path: Target file path.
        content: Text content to write.
        force: Whether to overwrite an existing file.
    """

    ensure_parent_dir(output_path)

    if output_path.exists() and not force:
        raise FileExistsError(
            f"{output_path} already exists. Use --force to overwrite it."
        )

    output_path.write_text(
        content,
        encoding = "utf-8"
    )


def build_placeholder_map(data):
    """Build a placeholder map for rendering.

    Args:
        data: Resume data loaded from JSON.
    """

    placeholders = {
        "name": "",
        "role_or_title": "",
        "city": "",
        "email": "",
        "phone": "",
        "website": "",
        "github": "",
        "linkedin": "",
        "summary_1": "",
        "summary_2": "",
        "summary_3": "",
        "school_1": "",
        "degree_1": "",
        "major_1": "",
        "education_time_1": "",
        "education_note_1": "",
        "company_1": "",
        "title_1": "",
        "experience_time_1": "",
        "team_1": "",
        "scope_1": "",
        "experience_bullet_1": "",
        "experience_bullet_2": "",
        "experience_bullet_3": "",
        "project_1": "",
        "project_role_1": "",
        "project_time_1": "",
        "project_stack_1": "",
        "project_scope_1": "",
        "project_bullet_1": "",
        "project_bullet_2": "",
        "project_bullet_3": "",
        "languages": "",
        "frameworks": "",
        "tools": "",
        "platforms": ""
    }

    basics = data.get("basics", {})
    placeholders["name"] = basics.get("name", "")
    placeholders["role_or_title"] = basics.get("title", "")
    placeholders["city"] = basics.get("city", "")
    placeholders["email"] = basics.get("email", "")
    placeholders["phone"] = basics.get("phone", "")
    placeholders["website"] = basics.get("website", "")
    placeholders["github"] = basics.get("github", "")
    placeholders["linkedin"] = basics.get("linkedin", "")

    summary = data.get("summary", [])
    for index, item in enumerate(summary[:3], start = 1):
        placeholders[f"summary_{index}"] = item

    education = data.get("education", [])
    if education:
        first = education[0]
        placeholders["school_1"] = first.get("school", "")
        placeholders["degree_1"] = first.get("degree", "")
        placeholders["major_1"] = first.get("major", "")
        placeholders["education_time_1"] = first.get("time", "")
        placeholders["education_note_1"] = first.get("note", "")

    experience = data.get("experience", [])
    if experience:
        first = experience[0]
        placeholders["company_1"] = first.get("company", "")
        placeholders["title_1"] = first.get("title", "")
        placeholders["experience_time_1"] = first.get("time", "")
        placeholders["team_1"] = first.get("team", "")
        placeholders["scope_1"] = first.get("scope", "")
        for index, item in enumerate(first.get("bullets", [])[:3], start = 1):
            placeholders[f"experience_bullet_{index}"] = item

    projects = data.get("projects", [])
    if projects:
        first = projects[0]
        placeholders["project_1"] = first.get("name", "")
        placeholders["project_role_1"] = first.get("role", "")
        placeholders["project_time_1"] = first.get("time", "")
        placeholders["project_stack_1"] = first.get("stack", "")
        placeholders["project_scope_1"] = first.get("scope", "")
        for index, item in enumerate(first.get("bullets", [])[:3], start = 1):
            placeholders[f"project_bullet_{index}"] = item

    skills = data.get("skills", {})
    placeholders["languages"] = ", ".join(skills.get("languages", []))
    placeholders["frameworks"] = ", ".join(skills.get("frameworks", []))
    placeholders["tools"] = ", ".join(skills.get("tools", []))
    placeholders["platforms"] = ", ".join(skills.get("platforms", []))

    return placeholders


def init_markdown_resume(
    output_path,
    force = False
):
    """Initialize a markdown resume file.

    Args:
        output_path: Target markdown path.
        force: Whether to overwrite an existing file.
    """

    content = MARKDOWN_TEMPLATE.format(**build_placeholder_map({}))
    write_text(
        output_path = output_path,
        content = content,
        force = force
    )


def render_markdown_resume(
    input_path,
    output_path,
    force = False
):
    """Render a markdown resume from JSON input.

    Args:
        input_path: Input JSON path.
        output_path: Output markdown path.
        force: Whether to overwrite an existing file.
    """

    data = json.loads(input_path.read_text(encoding = "utf-8"))
    content = MARKDOWN_TEMPLATE.format(**build_placeholder_map(data))
    write_text(
        output_path = output_path,
        content = content,
        force = force
    )


def render_latex_resume(
    input_path,
    output_path,
    force = False
):
    """Render a simplified LaTeX resume from JSON input.

    Args:
        input_path: Input JSON path.
        output_path: Output tex path.
        force: Whether to overwrite an existing file.
    """

    data = json.loads(input_path.read_text(encoding = "utf-8"))
    content = LATEX_TEMPLATE.format(**build_placeholder_map(data))
    write_text(
        output_path = output_path,
        content = content,
        force = force
    )


def main():
    """Run the CLI entry point."""

    args = parse_args()

    if args.command == "init-md":
        init_markdown_resume(
            output_path = Path(args.output),
            force = args.force
        )
        return

    if args.command == "render-md":
        render_markdown_resume(
            input_path = Path(args.input),
            output_path = Path(args.output),
            force = args.force
        )
        return

    if args.command == "render-tex":
        render_latex_resume(
            input_path = Path(args.input),
            output_path = Path(args.output),
            force = args.force
        )
        return

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
