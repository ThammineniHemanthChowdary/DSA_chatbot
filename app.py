# app.py
import gradio as gr
import pandas as pd
from core import problems
from core.runner import run_python
from core.complexity import analyze

def _func_name_from_signature(sig: str) -> str:
    after_def = sig.split("def", 1)[1].strip()
    return after_def.split("(", 1)[0].strip()

def load_problem(slug: str):
    p = problems.get(slug)
    title = f"### {p['title']}  \n**Difficulty:** {p.get('difficulty','?')}  \n**Patterns:** {', '.join(p.get('patterns', []))}"
    sig = p["signature"]
    samp_in = p["samples"][0]["input"] if p.get("samples") else {}
    samp_out = p["samples"][0]["output"] if p.get("samples") else {}
    starter = f"{sig}\n    # TODO: write your solution\n    pass\n"
    return title, sig, samp_in, samp_out, starter

def run_tests(slug: str, user_code: str):
    # 1) Run functional tests
    p = problems.get(slug)
    fn = _func_name_from_signature(p["signature"])
    tests = p.get("samples", []) + p.get("hidden_tests", [])

    res = run_python(user_code, fn, tests, timeout_s=3)
    if not res.get("ok"):
        empty_df = pd.DataFrame(columns=["n", "ms"])
        return (
            {
                "tests": {"status": "error", "message": res.get("error", "Unknown error")},
                "performance": None,
                "complexity": None
            },
            empty_df
        )

    expected = [t["output"] for t in tests]
    got = res["results"]
    verdicts, passed = [], True
    for i, (e, g) in enumerate(zip(expected, got)):
        ok = (e == g)
        passed &= ok
        verdicts.append({"case": i + 1, "expected": e, "got": g, "pass": ok})

    perf = {
        "elapsed_ms_total": res.get("elapsed_ms"),
        "peak_mem_kb": res.get("peak_mem_kb"),
    }

    # 2) Complexity analysis (static + empirical)
    analysis = analyze(user_code, fn, slug)

    # 3) Build DataFrame for LinePlot
    points = analysis.get("empirical_points") or []   # e.g., [(200, 1), (2000, 5), (8000, 19)]
    plot_rows = [
        {"n": int(n), "ms": (int(t) if (t is not None and t > 0) else None)}
        for (n, t) in points
    ]
    plot_df = pd.DataFrame(plot_rows, columns=["n", "ms"])

    result_json = {
        "tests": {"status": "ok" if passed else "fail", "details": verdicts},
        "performance": perf,
        "complexity": analysis
    }
    return result_json, plot_df

# ---------------- UI ----------------
with gr.Blocks(title="DSA Study Buddy") as demo:
    gr.Markdown("# 🧠 DSA Study Buddy\nLearn → Hint → Implement → Test")

    slugs = problems.list_slugs()
    default_slug = slugs[0] if slugs else None

    with gr.Row():
        slug = gr.Dropdown(choices=slugs, value=default_slug, label="Problem")
        load_btn = gr.Button("Load Problem")

    title_md = gr.Markdown()
    signature = gr.Code(language="python", interactive=False)
    with gr.Row():
        in_example = gr.JSON(label="Sample Input")
        out_example = gr.JSON(label="Sample Output")

    gr.Markdown("### Your Attempt")
    code = gr.Code(label="Write your Python 3 solution here", language="python", lines=18)

    run_btn = gr.Button("Run & Test")

    results = gr.JSON(label="Results")

    # Empirical runtime plot (Gradio 4.x)
    runtime_plot = gr.LinePlot(
        x="n",
        y="ms",
        label="Empirical runtime (ms vs n)",
        height=260,
        tooltip=["n", "ms"]
    )

    load_btn.click(load_problem, [slug], [title_md, signature, in_example, out_example, code])
    # run_tests returns TWO outputs: (results_json, pandas.DataFrame)
    run_btn.click(run_tests, [slug, code], [results, runtime_plot])

demo.launch()
