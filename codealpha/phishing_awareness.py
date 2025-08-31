# phishing_awareness.py
# Single-file Flask app: lesson + examples + interactive quiz
# Requirements: pip install flask

from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

LESSON_HTML = """
<h2>What is Phishing?</h2>
<p>Phishing is a social-engineering attack where attackers try to trick you into giving sensitive data (passwords, financial info) or executing actions (clicking malicious links, downloading attachments).</p>

<h3>How to recognize phishing emails & fake websites</h3>
<ul>
  <li><strong>Check the sender address:</strong> Look beyond the display name. Is the domain slightly misspelled?</li>
  <li><strong>Urgency & fear:</strong> Messages forcing immediate action ("Your account will be closed") are suspicious.</li>
  <li><strong>Unexpected attachments or links:</strong> Don't open or click without verifying.</li>
  <li><strong>Generic greetings:</strong> "Dear user" instead of your real name can be a sign.</li>
  <li><strong>Look for HTTPS and correct domain:</strong> but remember HTTPS alone is not proof of legitimacy.</li>
  <li><strong>Hover links:</strong> Hover (without clicking) to see the actual link target.</li>
</ul>

<h3>Social engineering tactics</h3>
<ul>
  <li><strong>Impersonation:</strong> Pretending to be a colleague, boss, or known service provider.</li>
  <li><strong>Authority & urgency:</strong> Pretending to be IT or security requesting immediate password change.</li>
  <li><strong>Scarcity / reward:</strong> "You've won" or "Limited offer" to override caution.</li>
</ul>

<h3>Best practices</h3>
<ul>
  <li>Don't click suspicious links—type the site URL yourself.</li>
  <li>Verify via another channel (phone, IM) if you get unusual requests from colleagues.</li>
  <li>Use unique passwords + a password manager.</li>
  <li>Enable multi-factor authentication (MFA).</li>
  <li>Keep software and antivirus up to date.</li>
  <li>Report suspected phishing to your IT/security team.</li>
</ul>
"""

EXAMPLES = [
    {
        "title": "Example 1 — Fake bank alert",
        "email": (
            "From: security@bank-secure.com\n"
            "Subject: Your account will be locked\n\n"
            "Dear Customer,\n"
            "We detected suspicious activity. Click here to verify your account now: http://bank-verify.example/login\n"
            "Failure to verify will lock your accounts."
        ),
        "why": "The domain is suspicious, the message creates urgency, and the link is not the official bank domain."
    },
    {
        "title": "Example 2 — CEO urgent payment request (spear-phish)",
        "email": (
            "From: ceo@yourcompany.com\n"
            "Subject: Urgent — Wire transfer\n\n"
            "Hi,\n"
            "I need you to transfer $15,000 to the account in the attached instructions immediately. Don't discuss this with anyone.\n"
            "Regards,\nCEO"
        ),
        "why": "Impersonation + instruction to bypass normal controls. Verify by calling the CEO directly using a known number."
    },
    {
        "title": "Example 3 — Software update with attachment",
        "email": (
            "From: updates@trusted-software.com\n"
            "Subject: Critical security update (attached)\n\n"
            "Please open the attached file to install the critical update."
        ),
        "why": "Unexpected attachments are risky. Software vendors rarely send updates via email attachments—use official update channels."
    }
]

QUIZ_QUESTIONS = [
    {
        "q": "You receive an email from your bank asking you to click a link and sign in to avoid account suspension. What are the best first steps? (choose the best single answer)",
        "options": [
            "Click the link and sign in to avoid suspension.",
            "Ignore it entirely.",
            "Hover the link to inspect URL and contact the bank using a known channel to verify.",
            "Reply to the email asking if it's legitimate."
        ],
        "a": 2
    },
    {
        "q": "A message from your CEO asks for an urgent wire transfer and says 'don't mention this to anyone'. What should you do?",
        "options": [
            "Send the wire immediately to be helpful.",
            "Verify the request by calling the CEO using a phone number you already have.",
            "Reply to the email asking for account number again.",
            "Forward to the finance team without question."
        ],
        "a": 1
    },
    {
        "q": "Which of these is the least reliable indicator of a website's legitimacy?",
        "options": [
            "HTTPS padlock in the address bar.",
            "Correct registered company domain and content.",
            "Unexpected pop-ups requesting credentials.",
            "Receiving the site link only from a trusted source."
        ],
        "a": 0
    }
]

INDEX_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Phishing Awareness Training</title>
  <meta charset="utf-8">
  <style>
    body { font-family: Arial, sans-serif; max-width:900px; margin:20px auto; line-height:1.5; }
    header { display:flex; align-items:center; gap:16px; }
    .card { background:#f8f8f8; padding:14px; border-radius:8px; margin-bottom:12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    pre { background:#111; color:#cfc; padding:10px; border-radius:6px; overflow:auto; }
    .nav { margin-top:8px; }
    a.button { background:#246; color:#fff; padding:8px 12px; border-radius:6px; text-decoration:none; }
  </style>
</head>
<body>
  <header>
    <h1>Phishing Awareness Training</h1>
  </header>

  <div class="card">
    {{ lesson|safe }}
    <div class="nav">
      <a class="button" href="{{ url_for('examples') }}">Real-world examples</a>
      <a class="button" href="{{ url_for('quiz') }}">Take the quiz</a>
    </div>
  </div>

  <div class="card">
    <h3>Quick checklist</h3>
    <ul>
      <li>Stop — think — verify.</li>
      <li>Check sender address and hover links.</li>
      <li>Never share credentials by email.</li>
      <li>Use MFA and a password manager.</li>
    </ul>
  </div>

  <footer style="font-size:0.9em; color:#555">
    Tip: run this locally and open <code>/</code> then try the quiz to test yourself.
  </footer>
</body>
</html>
"""

EXAMPLES_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Examples — Phishing Awareness</title>
  <meta charset="utf-8">
  <style>
    body { font-family: Arial, sans-serif; max-width:900px; margin:20px auto; }
    .card { background:#f8f8f8; padding:12px; border-radius:8px; margin-bottom:12px; }
    pre { background:#111; color:#cfc; padding:10px; border-radius:6px; overflow:auto; }
    a.button { background:#246; color:#fff; padding:8px 12px; border-radius:6px; text-decoration:none; }
  </style>
</head>
<body>
  <h1>Real-world phishing examples</h1>
  {% for ex in examples %}
  <div class="card">
    <h3>{{ ex.title }}</h3>
    <pre>{{ ex.email }}</pre>
    <strong>Why this is suspicious:</strong>
    <p>{{ ex.why }}</p>
  </div>
  {% endfor %}
  <a class="button" href="{{ url_for('index') }}">Back to lesson</a>
  <a class="button" href="{{ url_for('quiz') }}">Take the quiz</a>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Quiz — Phishing Awareness</title>
  <meta charset="utf-8">
  <style>
    body { font-family: Arial, sans-serif; max-width:900px; margin:20px auto; }
    .card { background:#f8f8f8; padding:12px; border-radius:8px; margin-bottom:12px; }
    label { display:block; margin:8px 0; }
    input[type=submit] { background:#246; color:#fff; padding:8px 12px; border-radius:6px; border:none; cursor:pointer; }
    .score { font-size:1.2em; font-weight:700; }
  </style>
</head>
<body>
  <h1>Interactive Quiz</h1>

  <form method="post" action="{{ url_for('quiz') }}">
    {% for i,q in enumerate(questions) %}
      <div class="card">
        <p><strong>Q{{ i+1 }}.</strong> {{ q.q }}</p>
        {% for j,opt in enumerate(q.options) %}
          <label><input type="radio" name="q{{i}}" value="{{j}}" required> {{ opt }}</label>
        {% endfor %}
      </div>
    {% endfor %}
    <input type="submit" value="Submit answers">
  </form>

  <p><a href="{{ url_for('index') }}">Back to lesson</a> | <a href="{{ url_for('examples') }}">Examples</a></p>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Quiz Results</title>
  <meta charset="utf-8">
  <style>
    body { font-family: Arial, sans-serif; max-width:900px; margin:20px auto; }
    .card { background:#f8f8f8; padding:12px; border-radius:8px; margin-bottom:12px; }
    .correct { color: green; font-weight:700; }
    .wrong { color: red; font-weight:700; }
  </style>
</head>
<body>
  <h1>Your Quiz Results</h1>
  <div class="card">
    <p class="score">Score: {{ score }} / {{ total }}</p>
    <ol>
    {% for i,res in enumerate(results) %}
      <li>
        <strong>Q{{ i+1 }}.</strong> {{ res.question }}<br>
        <span class="{{ 'correct' if res.correct else 'wrong' }}">{{ 'Correct' if res.correct else 'Incorrect' }}</span><br>
        Your answer: {{ res.your_answer }} <br>
        Correct answer: {{ res.correct_answer }}
      </li>
    {% endfor %}
    </ol>
  </div>

  <a href="{{ url_for('quiz') }}">Try again</a> | <a href="{{ url_for('index') }}">Back to lesson</a>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE, lesson=LESSON_HTML)

@app.route("/examples")
def examples():
    return render_template_string(EXAMPLES_TEMPLATE, examples=EXAMPLES)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "GET":
        return render_template_string(QUIZ_TEMPLATE, questions=QUIZ_QUESTIONS)
    # POST: grade
    total = len(QUIZ_QUESTIONS)
    score = 0
    results = []
    for i, q in enumerate(QUIZ_QUESTIONS):
        key = f"q{i}"
        val = request.form.get(key)
        try:
            chosen = int(val)
        except:
            chosen = None
        correct = (chosen == q["a"])
        if correct:
            score += 1
        results.append({
            "question": q["q"],
            "your_answer": q["options"][chosen] if chosen is not None and 0 <= chosen < len(q["options"]) else "No answer",
            "correct_answer": q["options"][q["a"]],
            "correct": correct
        })
    return render_template_string(RESULT_TEMPLATE, score=score, total=total, results=results)

if __name__ == "__main__":
    print("Starting Phishing Awareness web app on http://127.0.0.1:5000")
    app.run(debug=True)

