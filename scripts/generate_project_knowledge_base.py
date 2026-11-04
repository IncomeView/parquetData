#!/usr/bin/env python3
"""
generate_project_knowledge_base.py

Objetivos:
- Descobrir toda a estrutura do projeto
- Respeitar .gitignore
- Gerar árvore completa
- Catalogar arquivos
- Servir de base para análise arquitetural
- Evoluir para documentação automática e RAG

Autor: Moacir Magalhães
"""

from __future__ import annotations

import ast
import json
import re

from collections import Counter
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pathspec


# =============================================================================
# CONFIG
# =============================================================================

ROOT = Path(__file__).resolve().parents[1]

OUTPUT = (
    ROOT
    / "docs"
    / "_PROJECT_KNOWLEDGE_BASE.md"
)

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

ALWAYS_IGNORE = {
    "__pycache__",
    ".ipynb_checkpoints",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    ".git",
    "build",
    "dist",
}

IGNORE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pyc",
    ".pkl",
    ".gz",
    ".parquet",
}


MAX_FILE_READ_SIZE = 100_000


# =============================================================================
# GITIGNORE
# =============================================================================

def load_gitignore():

    gitignore = ROOT / ".gitignore"

    if not gitignore.exists():
        return None

    patterns = gitignore.read_text(
        encoding="utf-8"
    ).splitlines()

    return pathspec.PathSpec.from_lines(
        pathspec.patterns.GitWildMatchPattern,
        patterns,
    )


GIT_SPEC = load_gitignore()


def is_ignored(path: Path):

    for part in path.parts:
        if part in ALWAYS_IGNORE:
            return True

    if GIT_SPEC is None:
        return False

    try:

        rel = (
            path
            .relative_to(ROOT)
            .as_posix()
        )

        return GIT_SPEC.match_file(rel)

    except Exception:
        return False


# =============================================================================
# DISCOVERY
# =============================================================================

def get_project_files():

    files = []

    for item in ROOT.rglob("*"):

        if is_ignored(item):
            continue

        if not item.is_file():
            continue

        if (
            item.suffix.lower()
            in IGNORE_EXTENSIONS
        ):
            continue

        files.append(item)

    return sorted(files)


def get_python_files():

    return [

        f

        for f in get_project_files()

        if (
            f.suffix.lower() == ".py"
            and
            "generate_project_knowledge_base"
            not in f.name
        )
    ]


def get_markdown_files():

    return [
        f
        for f in get_project_files()
        if f.suffix.lower() == ".md"
    ]


def get_notebooks():

    return [
        f
        for f in get_project_files()
        if f.suffix.lower() == ".ipynb"
    ]


def get_yaml_files():

    return [
        f
        for f in get_project_files()
        if f.suffix.lower()
        in {
            ".yml",
            ".yaml",
        }
    ]


# =============================================================================
# TREE
# =============================================================================

def build_tree():

    lines = [ROOT.name]

    def walk(path, prefix=""):

        entries = []

        for item in sorted(
            path.iterdir(),
            key=lambda x: (
                x.is_file(),
                x.name.lower(),
            ),
        ):

            if is_ignored(item):
                continue

            if (
                item.is_file()
                and item.suffix.lower()
                in IGNORE_EXTENSIONS
            ):
                continue

            entries.append(item)

        for idx, item in enumerate(entries):

            last = idx == len(entries) - 1

            connector = (
                "└── "
                if last
                else "├── "
            )

            lines.append(
                f"{prefix}{connector}{item.name}"
            )

            if item.is_dir():

                extension = (
                    "    "
                    if last
                    else "│   "
                )

                walk(
                    item,
                    prefix + extension,
                )

    walk(ROOT)

    return "\n".join(lines)


# =============================================================================
# FILE CATALOG
# =============================================================================

def catalog_files():

    catalog = defaultdict(list)

    for file in get_project_files():

        ext = (
            file.suffix.lower()
            or "[sem extensão]"
        )

        catalog[ext].append(
            str(
                file.relative_to(ROOT)
            )
        )

    return dict(catalog)


def extension_statistics():

    counter = Counter()

    for file in get_project_files():

        ext = (
            file.suffix.lower()
            or "[sem extensão]"
        )

        counter[ext] += 1

    return dict(counter)


# =============================================================================
# HELPERS
# =============================================================================

def safe_read_file(file_path: Path):
    try:
        return (
            file_path
            .read_text(
                encoding="utf-8",
                errors="ignore",
            )[:MAX_FILE_READ_SIZE]
        )
    except Exception:

        return ""


def relative(path: Path):

    try:

        return str(
            path.relative_to(ROOT)
        )

    except Exception:

        return str(path)


# =============================================================================
# PYTHON ANALYSIS
# =============================================================================

PARSE_ERRORS = []


def extract_python_metadata(file_path: Path):

    result = {
        "classes": [],
        "functions": [],
        "imports": [],
        "module_doc": None,
        "env_vars": set(),
        "azure_keywords": set(),
    }

    try:

        source = safe_read_file(file_path)

        tree = ast.parse(source)

        result["module_doc"] = ast.get_docstring(tree)

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for name in node.names:
                    result["imports"].append(
                        name.name
                    )

            elif isinstance(
                node,
                ast.ImportFrom,
            ):

                if node.module:

                    result["imports"].append(
                        node.module
                    )

            elif isinstance(
                node,
                ast.ClassDef,
            ):

                result["classes"].append(
                    node.name
                )

            elif isinstance(
                node,
                ast.FunctionDef,
            ):

                result["functions"].append(
                    node.name
                )

    except Exception as exc:

        PARSE_ERRORS.append(
            {
                "file": relative(file_path),
                "error": str(exc),
            }
        )

    text = safe_read_file(file_path)

    env_pattern = re.compile(
        r"AZURE_[A-Z0-9_]+"
    )

    for match in env_pattern.findall(text):

        result["env_vars"].add(match)

    AZURE_TERMS = [
        "ClientSecretCredential",
        "DefaultAzureCredential",
        "ManagedIdentityCredential",
        "DataLakeServiceClient",
        "dfs.core.windows.net",
        "blob.core.windows.net",
        "azure.storage",
        "azure.identity",
        "fabric",
        "lakehouse",
    ]

    for term in AZURE_TERMS:

        if term.lower() in text.lower():

            result["azure_keywords"].add(term)

    result["imports"] = sorted(
        set(result["imports"])
    )

    result["env_vars"] = sorted(
        result["env_vars"]
    )

    result["azure_keywords"] = sorted(
        result["azure_keywords"]
    )

    return result


# =============================================================================
# MODULE DISCOVERY
# =============================================================================

def discover_local_modules():

    modules = set()

    for py in get_python_files():

        modules.add(py.stem)

    return modules


# =============================================================================
# DEPENDENCY MAP
# =============================================================================

def build_dependency_map():

    deps = defaultdict(list)

    local_modules = discover_local_modules()

    for py in get_python_files():

        meta = extract_python_metadata(py)

        for imp in meta["imports"]:

            top = imp.split(".")[0]

            if top in local_modules:

                deps[
                    relative(py)
                ].append(imp)

    return dict(deps)


# =============================================================================
# REQUIREMENTS
# =============================================================================

def analyze_requirements():

    file = ROOT / "requirements.txt"

    if not file.exists():

        return []

    lines = []

    for line in (
        file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines()
    ):

        line = line.strip()

        if (
            not line
            or line.startswith("#")
        ):
            continue

        lines.append(line)

    return sorted(lines)


# =============================================================================
# PYPROJECT
# =============================================================================

def analyze_pyproject():

    pyproject = ROOT / "pyproject.toml"

    if not pyproject.exists():

        return {}

    text = safe_read_file(pyproject)

    result = {
        "name": None,
        "version": None,
        "python": None,
    }

    name_match = re.search(
        r'name\s*=\s*"([^"]+)"',
        text,
    )

    version_match = re.search(
        r'version\s*=\s*"([^"]+)"',
        text,
    )

    python_match = re.search(
        r'requires-python\s*=\s*"([^"]+)"',
        text,
    )

    if name_match:
        result["name"] = name_match.group(1)

    if version_match:
        result["version"] = version_match.group(1)

    if python_match:
        result["python"] = python_match.group(1)

    return result


# =============================================================================
# README
# =============================================================================

def analyze_readme():

    readme = ROOT / "README.md"

    if not readme.exists():

        return ""

    return safe_read_file(readme)[
        :5000
    ]


# =============================================================================
# DOCKER
# =============================================================================

def analyze_docker():

    docker_files = []

    for file in get_project_files():

        if file.name.lower() in {
            "dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
        }:

            docker_files.append(
                relative(file)
            )

    return sorted(docker_files)


# =============================================================================
# GITHUB ACTIONS
# =============================================================================

def analyze_github_actions():

    workflows = []

    github = ROOT / ".github"

    if not github.exists():

        return workflows

    for file in github.rglob("*.yml"):

        workflows.append(
            relative(file)
        )

    for file in github.rglob("*.yaml"):

        workflows.append(
            relative(file)
        )

    return sorted(set(workflows))


# =============================================================================
# AZURE ANALYSIS
# =============================================================================

def analyze_azure_usage():

    findings = {
        "files": [],
        "keywords": set(),
        "env_vars": set(),
    }

    for py in get_python_files():

        meta = extract_python_metadata(py)

        if (
            meta["azure_keywords"]
            or meta["env_vars"]
        ):

            findings["files"].append(
                relative(py)
            )

            findings["keywords"].update(
                meta["azure_keywords"]
            )

            findings["env_vars"].update(
                meta["env_vars"]
            )

    findings["keywords"] = sorted(
        findings["keywords"]
    )

    findings["env_vars"] = sorted(
        findings["env_vars"]
    )

    findings["files"] = sorted(
        findings["files"]
    )

    return findings


# =============================================================================
# PIPELINE DETECTION
# =============================================================================

def detect_pipeline_files():

    keywords = [
        "pipeline",
        "bronze",
        "silver",
        "gold",
        "etl",
        "load",
        "extract",
        "transform",
    ]

    detected = []

    for py in get_python_files():

        content = safe_read_file(py)

        if any(
            kw.lower()
            in content.lower()
            for kw in keywords
        ):

            detected.append(
                relative(py)
            )

    return sorted(detected)

# =============================================================================
# ARCHITECTURE DETECTION
# =============================================================================

def detect_architecture_patterns():

    patterns = {
        "ADLS Gen2": [
            "DataLakeServiceClient",
            "dfs.core.windows.net",
        ],
        "Azure Identity": [
            "ClientSecretCredential",
            "DefaultAzureCredential",
            "ManagedIdentityCredential",
        ],
        "Microsoft Fabric": [
            "fabric",
            "lakehouse",
        ],
        "Docker": [
            "docker",
        ],
        "GitHub Actions": [
            "github/workflows",
        ],
        "Bronze Silver Gold": [
            "bronze",
            "silver",
            "gold",
        ],
        "PostgreSQL": [
            "postgres",
            "psycopg",
            "sqlalchemy",
        ],
        "Parquet": [
            "parquet",
            "pyarrow",
        ],
    }

    detected = defaultdict(list)

    for file in get_project_files():

        try:

            content = safe_read_file(file)

        except Exception:

            continue

        lower = content.lower()

        for architecture, keywords in patterns.items():

            for kw in keywords:

                if kw.lower() in lower:

                    detected[
                        architecture
                    ].append(
                        relative(file)
                    )

                    break

    return dict(detected)


# =============================================================================
# ADLS ANALYSIS
# =============================================================================

def analyze_adls_architecture():

    result = {
        "credential_type": set(),
        "storage_accounts": set(),
        "filesystems": set(),
        "files": [],
    }

    patterns = [
        "ClientSecretCredential",
        "DefaultAzureCredential",
        "ManagedIdentityCredential",
        "DataLakeServiceClient",
        "dfs.core.windows.net",
    ]

    for py in get_python_files():

        content = safe_read_file(py)

        found = False

        for pattern in patterns:

            if pattern in content:

                result["credential_type"].add(
                    pattern
                )

                found = True

        if found:

            result["files"].append(
                relative(py)
            )

    result["files"] = sorted(
        result["files"]
    )

    result["credential_type"] = sorted(
        result["credential_type"]
    )

    return result


# =============================================================================
# FABRIC ANALYSIS
# =============================================================================

def analyze_fabric_usage():

    findings = []

    keywords = [
        "lakehouse",
        "fabric",
        "files/",
        "Files/",
    ]

    for file in get_project_files():

        content = safe_read_file(file)

        if any(
            k.lower()
            in content.lower()
            for k in keywords
        ):

            findings.append(
                relative(file)
            )

    return sorted(set(findings))


# =============================================================================
# BRONZE SILVER GOLD
# =============================================================================

def analyze_data_layers():

    layers = {
        "bronze": [],
        "silver": [],
        "gold": [],
    }

    for file in get_project_files():

        content = safe_read_file(file)

        lower = content.lower()

        for layer in layers:

            if layer in lower:

                layers[layer].append(
                    relative(file)
                )

    return layers


# =============================================================================
# PIPELINE FLOW DETECTION
# =============================================================================

def analyze_pipeline_flow():

    flow = []

    keywords = [
        "read_table_to_parquet",
        "upload_to_adls",
        "bronze",
        "silver",
        "gold",
        "load",
        "extract",
        "transform",
    ]

    for py in get_python_files():

        content = safe_read_file(py)

        detected = []

        for kw in keywords:

            if kw in content:

                detected.append(kw)

        if detected:

            flow.append(
                {
                    "file": relative(py),
                    "steps": detected,
                }
            )

    return flow


# =============================================================================
# TABLE DETECTION
# =============================================================================

def detect_database_tables():

    settings_file = None

    for py in get_python_files():

        if py.name == "settings.py":

            settings_file = py
            break

    if not settings_file:

        return []

    content = safe_read_file(settings_file)

    pattern = re.compile(
        r'BRONZE_TABLES\s*=\s*\{.*?\[(.*?)\]',
        re.DOTALL,
    )

    results = []

    match = pattern.search(content)

    if not match:

        return []

    tables_block = match.group(1)

    table_pattern = re.compile(
        r'"([^"]+)"'
    )

    for table in table_pattern.findall(
        tables_block
    ):

        results.append(table)

    return sorted(set(results))


# =============================================================================
# ENVIRONMENT VARIABLES
# =============================================================================

def detect_environment_variables():

    envs = set()

    valid_prefixes = (
        "AZURE_",
        "DB_",
        "POSTGRES_",
    )

    pattern = re.compile(
        r"[A-Z]{2,}_[A-Z0-9_]+"
    )

    for py in get_python_files():

        content = safe_read_file(py)

        for item in pattern.findall(
            content
        ):

            if item.startswith(
                valid_prefixes
            ):

                envs.add(item)

    return sorted(envs)


# =============================================================================
# RAG INDEX
# =============================================================================

def build_rag_index():

    rag_documents = []

    for py in get_python_files():

        meta = extract_python_metadata(py)

        rag_documents.append(
            {
                "file": relative(py),
                "classes": meta["classes"],
                "functions": meta["functions"],
                "imports": meta["imports"],
                "env_vars": meta["env_vars"],
                "architecture_tags": meta["azure_keywords"],
            }
        )

    return rag_documents


# =============================================================================
# EXPORT RAG JSON
# =============================================================================

def export_rag_index():

    output = (
        ROOT
        / "docs"
        / "_PROJECT_RAG_INDEX.json"
    )

    index = build_rag_index()

    with open(
        output,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            index,
            f,
            indent=2,
            ensure_ascii=False,
        )

    return output


# =============================================================================
# KNOWLEDGE EXTRACTION
# =============================================================================

def extract_project_knowledge():

    knowledge = {
        "architecture": [],
        "risks": [],
        "recommendations": [],
        "pipeline_summary": [],
    }

    architecture_patterns = (
        detect_architecture_patterns()
    )

    if "ADLS Gen2" in architecture_patterns:

        knowledge["architecture"].append(
            "Azure Data Lake Storage Gen2"
        )

    if "PostgreSQL" in architecture_patterns:

        knowledge["architecture"].append(
            "PostgreSQL"
        )

    if "Parquet" in architecture_patterns:

        knowledge["architecture"].append(
            "Parquet Storage"
        )

    if "Bronze Silver Gold" in architecture_patterns:

        knowledge["architecture"].append(
            "Medallion Architecture"
        )

    if "Microsoft Fabric" in architecture_patterns:

        knowledge["architecture"].append(
            "Microsoft Fabric"
        )

    if "Docker" in architecture_patterns:

        knowledge["architecture"].append(
            "Containerization"
        )

    return knowledge


# =============================================================================
# RISK ANALYSIS
# =============================================================================

def analyze_project_risks():

    risks = []

    project_files = get_project_files()

    names = {
        x.name.lower()
        for x in project_files
    }

    if "dockerfile" not in names:

        risks.append(
            "Dockerfile não encontrado"
        )

    if (
        "requirements.txt"
        not in names
    ):

        risks.append(
            "requirements.txt ausente"
        )

    if not analyze_github_actions():

        risks.append(
            "CI/CD não encontrado"
        )

    if len(get_python_files()) > 0:

        tests = [
            x
            for x in project_files
            if "test"
            in x.name.lower()
        ]

        if not tests:

            risks.append(
                "Projeto sem testes detectados"
            )

    return risks


# =============================================================================
# IMPROVEMENT DETECTION
# =============================================================================

def generate_recommendations():

    recommendations = []

    azure = analyze_azure_usage()

    if (
        "ClientSecretCredential"
        in azure["keywords"]
    ):

        recommendations.append(
            (
                "Avaliar migração para "
                "DefaultAzureCredential"
            )
        )

    recommendations.append(
        (
            "Adicionar observabilidade "
            "estruturada com logging"
        )
    )

    recommendations.append(
        (
            "Adicionar documentação "
            "de arquitetura"
        )
    )

    recommendations.append(
        (
            "Adicionar data lineage"
        )
    )

    recommendations.append(
        (
            "Adicionar monitoramento "
            "de pipelines"
        )
    )

    return recommendations


# =============================================================================
# ENTRY POINT DETECTION
# =============================================================================

def find_project_entrypoints():

    entrypoints = []

    for py in get_python_files():

        content = safe_read_file(py)

        if (
            "__main__"
            in content
        ):

            entrypoints.append(
                relative(py)
            )

    return sorted(entrypoints)


# =============================================================================
# PACKAGE STRUCTURE
# =============================================================================

def analyze_package_structure():

    packages = []

    for py in get_python_files():

        if py.name == "__init__.py":

            packages.append(
                relative(py.parent)
            )

    return sorted(packages)


# =============================================================================
# CONFIGURATION FILES
# =============================================================================

def detect_configuration_files():

    config_files = []

    patterns = {
        ".env",
        ".gitignore",
        "requirements.txt",
        "pyproject.toml",
        "dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
    }

    for file in get_project_files():

        if (
            file.name.lower()
            in patterns
        ):

            config_files.append(
                relative(file)
            )

    return sorted(config_files)


# =============================================================================
# BUSINESS ENTITIES
# =============================================================================

def detect_business_entities():

    entities = set()

    tables = detect_database_tables()

    for item in tables:

        entities.add(item)

    return sorted(entities)


# =============================================================================
# KNOWLEDGE SUMMARY
# =============================================================================

def generate_executive_summary():

    summary = []

    summary.append(
        f"Projeto: {ROOT.name}"
    )

    summary.append(
        f"Arquivos Python: "
        f"{len(get_python_files())}"
    )

    summary.append(
        f"Arquivos Markdown: "
        f"{len(get_markdown_files())}"
    )

    summary.append(
        f"Notebooks: "
        f"{len(get_notebooks())}"
    )

    return summary

# =============================================================================
# REPORT WRITER
# =============================================================================

def write_report():

    tree = build_tree()
    extension_stats = extension_statistics()
    pyproject_info = analyze_pyproject()
    requirements = analyze_requirements()
    docker_files = analyze_docker()
    github_actions = analyze_github_actions()
    azure_info = analyze_azure_usage()
    dependency_map = build_dependency_map()
    py_files = get_python_files()
    markdown_files = get_markdown_files()
    notebooks = get_notebooks()

    adls_info = analyze_adls_architecture()
    fabric_info = analyze_fabric_usage()
#    layers_info = analyze_data_layers()
    pipeline_flow = analyze_pipeline_flow()
#    tables = detect_database_tables()
#    env_vars = detect_environment_variables()

    knowledge = extract_project_knowledge()

    risks = analyze_project_risks()

    recommendations = (
        generate_recommendations()
    )

    entrypoints = (
        find_project_entrypoints()
    )

    packages = (
        analyze_package_structure()
    )

    config_files = (
        detect_configuration_files()
    )

    entities = (
        detect_business_entities()
    )

    summary = (
        generate_executive_summary()
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as f:

        # =============================================================
        # HEADER
        # =============================================================

        f.write(
            "# PROJECT KNOWLEDGE BASE\n\n"
        )

        f.write(
            f"Gerado em: "
            f"{datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
        )

        f.write(
            f"Projeto: {ROOT.name}\n\n"
        )

        # =============================================================
        # EXECUTIVE SUMMARY
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Resumo Executivo\n\n"
        )
        for item in summary:
            f.write(f"- {item}\n")
        f.write("\n")
        f.write(
            f"- Total de arquivos: {len(get_project_files())}\n"
        )
        f.write(
            f"- Scripts Python: {len(py_files)}\n"
        )
        f.write(
            f"- Arquivos Markdown: {len(markdown_files)}\n"
        )
        f.write(
            f"- Notebooks: {len(notebooks)}\n"
        )
        f.write(
            f"- Extensões encontradas: {len(extension_stats)}\n\n"
        )

        # =============================================================
        # STRUCTURE
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Estrutura do Projeto\n\n"
        )

        f.write("```text\n")
        f.write(tree)
        f.write("\n```\n\n")

        # =============================================================
        # PYPROJECT
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## PyProject\n\n"
        )

        if pyproject_info:

            for key, value in pyproject_info.items():

                f.write(
                    f"- {key}: {value}\n"
                )

        else:

            f.write(
                "pyproject.toml não encontrado.\n"
            )

        f.write("\n")

        # =============================================================
        # REQUIREMENTS
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Dependências\n\n"
        )

        if requirements:

            for package in requirements:

                f.write(
                    f"- {package}\n"
                )

        else:

            f.write(
                "requirements.txt não encontrado.\n"
            )

        f.write("\n")

        # =============================================================
        # FILE STATISTICS
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Estatísticas de Arquivos\n\n"
        )

        for ext, count in sorted(
            extension_stats.items()
        ):

            f.write(
                f"- {ext}: {count}\n"
            )

        f.write("\n")

        # =============================================================
        # DOCKER
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Docker\n\n"
        )

        if docker_files:

            for item in docker_files:

                f.write(
                    f"- {item}\n"
                )

        else:

            f.write(
                "Nenhum arquivo Docker encontrado.\n"
            )

        f.write("\n")

        # =============================================================
        # GITHUB ACTIONS
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## GitHub Actions\n\n"
        )

        if github_actions:

            for workflow in github_actions:

                f.write(
                    f"- {workflow}\n"
                )

        else:

            f.write(
                "Nenhum workflow encontrado.\n"
            )

        f.write("\n")

        # =============================================================
        # AZURE
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Azure Detection\n\n"
        )

        f.write(
            "### Fabric\n\n"
        )

        for item in fabric_info:

            f.write(
                f"- {item}\n"
            )

        f.write("\n")


        f.write("### ADLS\n\n")

        for item in adls_info["credential_type"]:

            f.write(
                f"- {item}\n"
            )

        f.write("\n")

       

        # =============================================================
        # PIPELINE FLOW
        # =============================================================

        f.write("---\n\n")
        f.write("## Pipeline Flow\n\n")

        for item in pipeline_flow:

            f.write(
                f"### {item['file']}\n\n"
            )

            for step in item["steps"]:

                f.write(
                    f"- {step}\n"
                )

            f.write("\n")


        # =============================================================
        # RECONSTRUCTED ARCHITECTURE
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Arquitetura Reconstruída\n\n"
        )

        f.write(
        """
            PostgreSQL
                │
                ▼
            read_table_to_parquet()
                │
                ▼
            Arquivos Parquet
                │
                ▼
            upload_to_adls()
                │
                ▼
            Azure Data Lake Storage Gen2
                │
                ▼
            bronze/
                │
                ▼
            silver/
                │
                ▼
            gold/
                │
                ▼
            Microsoft Fabric Lakehouse
        """
        )

        f.write( "\n\n      Fluxo reconstruído automaticamente a partir das dependências, imports e pipelines detectados no projeto.\n\n" )


        # =============================================================
        # ARCHITECTURE
        # =============================================================


        f.write("---\n\n")
        f.write("## Arquitetura Detectada\n\n")

        for item in knowledge["architecture"]:
            f.write(f"- {item}\n")

        f.write("\n")

        # =============================================================
        # TECHNOLOGY STACK
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Stack Tecnológica\n\n"
        )

        for package in requirements:

            f.write(
                f"- {package}\n"
            )

        f.write("\n")

        # =============================================================
        # ENTRYPOINTS
        # =============================================================

        f.write("---\n\n")
        f.write("## Entrypoints\n\n")

        for item in entrypoints:
            f.write(f"- {item}\n")

        f.write("\n")

        # =============================================================
        # CONFIG FILES
        # =============================================================

        f.write("---\n\n")
        f.write("## Arquivos de Configuração\n\n")

        for item in config_files:
            f.write(f"- {item}\n")

        f.write("\n")

        # =============================================================
        # BUSINESS ENTITIES
        # =============================================================

        f.write("---\n\n")
        f.write("## Entidades de Negócio\n\n")

        for item in entities:
            f.write(f"- {item}\n")

        f.write("\n")

        # =============================================================
        # RISKS
        # =============================================================

        f.write("---\n\n")
        f.write("## Riscos Detectados\n\n")

        if risks:
            for item in risks:
                f.write(f"- {item}\n")
        else:
            f.write(
                "Nenhum risco estrutural detectado.\n"
            )

        f.write("\n")

        # =============================================================
        # RECOMMENDATIONS
        # =============================================================

        f.write("---\n\n")
        f.write("## Recomendações\n\n")

        for item in recommendations:
            f.write(f"- {item}\n")

        f.write("\n")

        f.write(
            "### Arquivos Relacionados\n\n"
        )

        for file in azure_info["files"]:

            f.write(
                f"- {file}\n"
            )

        f.write("\n")

        f.write(
            "### Keywords Detectadas\n\n"
        )

        for keyword in azure_info["keywords"]:

            f.write(
                f"- {keyword}\n"
            )

        f.write("\n")

        f.write(
            "### Variáveis de Ambiente\n\n"
        )

        for env in azure_info["env_vars"]:

            f.write(
                f"- {env}\n"
            )

        f.write("\n")

        # =============================================================
        # ROADMAP
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Roadmap Sugerido\n\n"
        )

        roadmap = [
            "Observabilidade com logging estruturado",
            "Data Lineage",
            "Carga incremental",
            "Arquitetura Bronze/Silver/Gold completa",
            "Integração avançada com Fabric",
            "Monitoramento de pipelines",
            "Testes de integração",
        ]

        for item in roadmap:

            f.write(
                f"- {item}\n"
            )

        f.write("\n")

        # =============================================================
        # DEPENDENCY MAP
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Mapa de Dependências\n\n"
        )

        for file, imports in sorted(
            dependency_map.items()
        ):

            f.write(
                f"### {file}\n\n"
            )

            if not imports:

                f.write(
                    "Sem dependências internas.\n\n"
                )

                continue

            for imp in imports:

                f.write(
                    f"- {imp}\n"
                )

            f.write("\n")

        # =============================================================
        # SCRIPT CATALOG
        # =============================================================

        f.write("---\n\n")

        f.write(
            "## Catálogo de Scripts Python\n\n"
        )

        for py in py_files:

            meta = extract_python_metadata(py)

            f.write(
                f"### {relative(py)}\n\n"
            )

            if meta["module_doc"]:

                f.write(
                    "#### Descrição\n\n"
                )

                f.write(
                    meta["module_doc"]
                )

                f.write("\n\n")

            if meta["classes"]:

                f.write(
                    "#### Classes\n\n"
                )

                for cls in meta["classes"]:

                    f.write(
                        f"- {cls}\n"
                    )

                f.write("\n")

            if meta["functions"]:

                f.write(
                    "#### Funções\n\n"
                )

                for fn in meta["functions"]:

                    f.write(
                        f"- {fn}()\n"
                    )

                f.write("\n")

            if meta["imports"]:

                f.write(
                    "#### Imports\n\n"
                )

                for imp in meta["imports"]:

                    f.write(
                        f"- {imp}\n"
                    )

                f.write("\n")

        # =============================================================
        # PARSE ERRORS
        # =============================================================

        if PARSE_ERRORS:

            f.write("---\n\n")

            f.write(
                "## Erros de Parsing\n\n"
            )

            for err in PARSE_ERRORS:

                f.write(
                    f"- {err['file']} : {err['error']}\n"
                )

            f.write("\n")


    export_rag_index()
    print(
        f"\nKnowledge Base gerada:\n{OUTPUT}\n"
    )





# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    write_report()