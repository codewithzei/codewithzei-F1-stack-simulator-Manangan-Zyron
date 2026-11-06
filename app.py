"""Flask Stack Simulator."""
from secrets import token_hex

from flask import Flask, flash, redirect, render_template, request, session, url_for

from stack_model import Stack

app = Flask(__name__)
app.secret_key = token_hex(32)
app.config["SESSION_COOKIE_NAME"] = "stack_session"


@app.route('/')
def index():
    stack = Stack(session.get("stack_items", []))
    highlight = session.pop("peek", False)
    return render_template(
        "index.html",
        items=list(reversed(stack.items)),
        size=stack.size(),
        popped=session.get("popped_items", []),
        highlight=highlight,
    )


@app.route('/stack', methods=['POST'])
def operate():
    action = request.form.get("action", "")
    value = request.form.get("value", "").strip()
    stack = Stack(session.get("stack_items", []))
    popped = session.get("popped_items", [])
    session.pop("peek", None)

    if action == "push":
        if not value:
            flash("Enter a value before pushing.", "error")
        elif len(value) > 24:
            flash("Values can contain at most 24 characters.", "error")
        elif stack.size() >= 20:
            flash("The stack is full. It can hold at most 20 items.", "error")
        else:
            stack.push(value)
            flash(f"Pushed {value}.", "success")
    elif action == "pop":
        if stack.is_empty():
            flash("The stack is empty. Nothing to pop.", "error")
        else:
            removed = stack.pop()
            popped.insert(0, removed)
            popped = popped[:20]
            flash(f"Popped {removed}.", "success")
    elif action == "peek":
        if stack.is_empty():
            flash("The stack is empty. Nothing to peek.", "error")
        else:
            session["peek"] = True
            flash(f"The top item is {stack.peek()}.", "success")
    elif action == "clear":
        stack.clear()
        popped = []
        flash("The stack was cleared.", "success")
    else:
        flash("Unknown stack operation.", "error")

    session["stack_items"] = stack.items
    session["popped_items"] = popped
    return redirect(url_for("index"))


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run()
