from io import BytesIO
import base64
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pdfkit
import matplotlib.pyplot as plt 
# Add your wkhtmltopdf path if needed
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"

def generate_validation_report(data_dict, output_dir="reports/"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    html_out = os.path.join(output_dir, f"report_{timestamp}.html")
    pdf_out = os.path.join(output_dir, f"report_{timestamp}.pdf")

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    html_content = template.render(
        timestamp=timestamp,
        config=data_dict["config"],
        plots=data_dict["plots"]
    )

    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdfkit.from_file(html_out, pdf_out, configuration=config)
    print(f"✅ Report saved: {pdf_out}")
