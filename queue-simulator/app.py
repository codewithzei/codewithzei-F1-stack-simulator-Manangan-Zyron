"""Flask Queue Simulator."""
from secrets import token_hex

from flask import Flask, flash, redirect, render_template, request, session, url_for

from queue_model import Queue

app = Flask(__name__)
app.secret_key = token_hex(32)
app.config["SESSION_COOKIE_NAME"] = "queue_session"


@app.route('/')
def index():
    queue = Queue(session.get("queue_items", []))
    highlight = session.pop("peek", False)
    return render_template(
        "index.html",
        items=list(queue.items),
        size=queue.size(),
        removed=session.get("removed_items", []),
        highlight=highlight,
    )


@app.route('/queue', methods=['POST'])
def operate():
    action = request.form.get("action", "")
    value = request.form.get("value", "").strip()
    queue = Queue(session.get("queue_items", []))
    removed_items = session.get("removed_items", [])
    session.pop("peek", None)

    if action == "enqueue":
        if not value:
            flash("Enter a value before enqueueing.", "error")
        elif len(value) > 24:
            flash("Values can contain at most 24 characters.", "error")
        elif queue.size() >= 20:
            flash("The queue is full. It can hold at most 20 items.", "error")
        else:
            queue.enqueue(value)
            flash(f"Enqueued {value} at the rear.", "success")
    elif action == "dequeue":
        if queue.is_empty():
            flash("The queue is empty. Nothing to dequeue.", "error")
        else:
            removed = queue.dequeue()
            removed_items.insert(0, removed)
            removed_items = removed_items[:20]
            flash(f"Dequeued {removed} from the front.", "success")
    elif action == "peek":
        if queue.is_empty():
            flash("The queue is empty. Nothing to peek.", "error")
        else:
            session["peek"] = True
            flash(f"The front item is {queue.peek()}.", "success")
    elif action == "clear":
        queue.clear()
        removed_items = []
        flash("The queue was cleared.", "success")
    else:
        flash("Unknown queue operation.", "error")

    session["queue_items"] = queue.items
    session["removed_items"] = removed_items
    return redirect(url_for("index"))


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(port=5001)
