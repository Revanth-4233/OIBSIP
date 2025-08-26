from flask import Flask, request, render_template_string
import random
import string

app = Flask(__name__)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Password Generator</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      background: #f9f9f9;
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
    input, label {
      margin: 28px 0;
       font-size:30px;
    }
    input[type="number"] {
      width: 90%;
      font-size:30px;
      padding: 30px;
      border-radius: 6px;
      border: 2px solid #ccc;
    }
    button {
      width: 95%;
      padding: 30px;
      margin-top: 15px;
      background: #673ab7;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 30px;
    }
    button:hover {
      background: #5e35b1;
    }
    .result {
      margin-top: 20px;
      font-size: 30px;
      font-weight: bold;
      color: #2e7d32;
      word-break: break-word;
    }
    .options {
      text-align: left;
      margin-left: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🔑 Password Generator</h1>
    <form method="POST">
      <input type="number" name="length" placeholder="Enter password length" min="4" max="50" required><br>

      <div class="options">
        <label><input type="checkbox" name="letters" checked> Include Letters</label><br>
        <label><input type="checkbox" name="digits" checked> Include Digits</label><br>
        <label><input type="checkbox" name="symbols" checked> Include Symbols</label><br>
      </div>

      <button type="submit">Generate</button>
    </form>

    {% if password %}
      <div class="result">
        Your Password:<br> <b>{{ password }}</b>
      </div>
    {% endif %}
  </div>
</body>
</html>
"""

def generate_password(length=12, use_letters=True, use_digits=True, use_symbols=True):
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "Error: No character set selected!"

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route("/", methods=["GET", "POST"])
def password_generator():
    password = ""
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        use_letters = "letters" in request.form
        use_digits = "digits" in request.form
        use_symbols = "symbols" in request.form

        password = generate_password(length, use_letters, use_digits, use_symbols)

    return render_template_string(html_code, password=password)

if __name__ == "__main__":
    app.run(debug=True)
