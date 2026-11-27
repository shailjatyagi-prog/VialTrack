from flask import Flask, render_template, request
import os

app = Flask(__name__)

DATA_FILE = os.path.join("data", "samples.text")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        sample = {
            "sample_type": request.form.get("sample_type"),
            "description": request.form.get("description"),
            "incubator": request.form.get("incubator"),
            "shelf": request.form.get("shelf"),
            "rack": request.form.get("rack"),
            "box": request.form.get("box"),
            "position": request.form.get("position")
        }

        with open(DATA_FILE, "a") as file:
            file.write(
                f"\nSample Type: {sample['sample_type']}\n"
                f"Description: {sample['description']}\n"
                f"Incubator: {sample['incubator']}\n"
                f"Shelf: {sample['shelf']}\n"
                f"Rack: {sample['rack']}\n"
                f"Box: {sample['box']}\n"
                f"Position: {sample['position']}\n"
                "------------------------------\n"
            )

        return render_template("register.html", submitted=True, sample=sample)

    return render_template("register.html", submitted=False)


if __name__ == "__main__":
    app.run(debug=True)