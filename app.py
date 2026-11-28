
from flask import Flask, render_template, request
import os
import uuid

app = Flask(__name__)

DATA_FILE = os.path.join("data", "samples.text")


# helper function to check for duplicate storage locations
def location_exists(location):
    if not os.path.exists(DATA_FILE):
        return False

    with open(DATA_FILE, "r") as file:
        content = file.read()

    # check new-format records
    if f"Storage Location: {location}" in content:
        return True

    # check older-format records
    location_parts = [part.strip() for part in location.split("/")]

    incubator, shelf, rack, box, position = location_parts

    old_format_location = (
        f"Incubator: {incubator}\n"
        f"Shelf: {shelf}\n"
        f"Rack: {rack}\n"
        f"Box: {box}\n"
        f"Position: {position}"
    )

    return old_format_location in content


# homepage
@app.route("/")
def home():
    return render_template("index.html")


# sample registration form
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # collect sample information from the form
        sample = {
            "sample_id": str(uuid.uuid4())[:8].upper(),
            "sample_type": request.form.get("sample_type"),
            "description": request.form.get("description"),
            "incubator": request.form.get("incubator"),
            "shelf": request.form.get("shelf"),
            "rack": request.form.get("rack"),
            "box": request.form.get("box"),
            "position": request.form.get("position")
        }

        # organize storage location into one format
        sample["storage_location"] = (
            f"{sample['incubator']} / "
            f"{sample['shelf']} / "
            f"{sample['rack']} / "
            f"{sample['box']} / "
            f"{sample['position']}"
        )

        # check if the storage location is already occupied
        if location_exists(sample["storage_location"]):
            return render_template(
                "register.html",
                submitted=False,
                error="This storage location is already occupied. Please choose another location."
            )

        # save sample information to the data file
        with open(DATA_FILE, "a") as file:
            file.write(
                f"\nSample ID: {sample['sample_id']}\n"
                f"Sample Type: {sample['sample_type']}\n"
                f"Description: {sample['description']}\n"
                f"Storage Location: {sample['storage_location']}\n"
                "------------------------------\n"
            )

        # display successful registration confirmation
        return render_template(
            "register.html",
            submitted=True,
            sample=sample
        )

    return render_template("register.html", submitted=False)


# run the flask application
if __name__ == "__main__":
    app.run(debug=True)
