from flask import Flask, request, render_template_string

app = Flask(__name__)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BMI Calculator</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      background: #f2f2f2;
      margin: 0;
      padding: 0;
    }
    .container {
      background: #fff;
      width: 50%;
      height: 700px;
      margin: 80px auto;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    h2 {
      margin-bottom: 20px;
      color: #333;
    }
    input {
      width: 90%;
      font-size: 30px;
      padding: 30px;
      margin: 20px 0;
      border-radius: 6px;
      border: 1px solid #ccc;
    }
    button {
      width: 95%;
      padding: 30px;
      margin-top: 15px;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 36px;
    }
    button:hover {
      background: #45a049;
    }
    .result {
      margin-top: 30px;
      font-size: 38px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>BMI Calculator</h1>
    <form method="POST">
      <input type="number" name="weight" step="0.1" placeholder="Enter weight (kg)" required>
      <input type="number" name="height" step="0.1" placeholder="Enter height (feet)" required>
      <button type="submit">Calculate</button>
    </form>

    {% if bmi %}
      <div class="result">
        Your BMI is <b>{{ bmi }}</b> ({{ category }})
      </div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def bmi_calculator():
    bmi = None
    category = None

    if request.method == "POST":
        try:
            weight = float(request.form["weight"])   # in kg
            height_feet = float(request.form["height"])  # in feet

            if weight > 0 and height_feet > 0:
                # Convert feet → meters
                height_m = height_feet * 0.3048
                bmi = round(weight / (height_m * height_m), 2)

                # Categorization
                if bmi < 18.5:
                    category = "Underweight"
                elif bmi < 25:
                    category = "Normal weight"
                elif bmi < 30:
                    category = "Overweight"
                else:
                    category = "Obese"
        except:
            bmi = None

    return render_template_string(html_code, bmi=bmi, category=category)

if __name__ == "__main__":
    app.run(debug=True)
