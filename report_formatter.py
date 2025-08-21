def format_report_html(results: list) -> str:
    """
    Formats rule results into an HTML audit report.
    """
    if not results:
        return "<p>✅ No issues found. Estimate looks complete.</p>"

    html = []

    for result in results:
        rule = result.get("rule", "Unnamed Rule")
        suggestions = result.get("suggestions", [])

        html.append(f"<h3>🔍 {rule}</h3>")
        html.append("<ul>")

        for item in suggestions:
            html.append(f"<li>{item}</li>")

        html.append("</ul>")

    return "\n".join(html)