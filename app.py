import time

from flask import Flask, render_template, request
from agents.analyst_agent import analyze_bug
from agents.qa_agent import generate_bug_report
import markdown


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    title = request.form.get("title")
    description = request.form.get("description")
    master_img_b64 = request.form.get("screenshot_master")
    branch_img_b64 = request.form.get("screenshot_branch")

    print("\n🚀 Bug generation started...")
    start_time = time.time()

    analyst_findings = analyze_bug(title, description, master_img_b64, branch_img_b64)
    bug_report_text = generate_bug_report(title, description, analyst_findings,
                                          master_img_b64, branch_img_b64)

    html_output = markdown.markdown(bug_report_text)

    # Inject screenshots visually under the bug report text
    img_html = ""
    if master_img_b64:
        img_html += f'''
        <h3 style="color:#93c5fd;">Master Screenshot:</h3>
        <img src="{master_img_b64}" class="rounded border border-gray-700 mb-4" style="max-width:400px; height:auto;"/>
        '''
    if branch_img_b64:
        img_html += f'''
        <h3 style="color:#93c5fd;">Branch Screenshot:</h3>
        <img src="{branch_img_b64}" class="rounded border border-gray-700" style="max-width:400px; height:auto;"/>
        '''

    html_output = f"{html_output}<br>{img_html}"

    elapsed = time.time() - start_time
    print(f"✅ Bug generation completed in {elapsed:.2f} seconds.\n")

    return render_template(
        "index.html",
        bug=html_output,
        title=title,
        description=description,
        screenshot_master=master_img_b64,
        screenshot_branch=branch_img_b64
    )


if __name__ == "__main__":
    app.run(debug=True)
