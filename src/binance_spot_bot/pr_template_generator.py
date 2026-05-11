from .dev_quality_facade import safe_record
def pr_template(title: str): return safe_record("pr_template", {"title": title, "sections": ["summary", "tests", "safety"]})
