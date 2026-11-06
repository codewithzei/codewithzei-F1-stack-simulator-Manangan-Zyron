# Flask Stack and Queue Simulators

**Name:** MANANGAN, ZYRON T.  
**Section:** BSIT WMT IV - 2  
**GitHub Repository:** https://github.com/codewithzei/codewithzei-F1-stack-simulator-Manangan-Zyron

This repository contains two separate Flask applications:

- The root application is a **Stack Simulator** using LIFO behavior.
- `queue-simulator/` is a **Queue Simulator** using FIFO behavior.

## Stack Simulator

From the repository root:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Supported operations:

- **Push** adds a value to the top of the stack.
- **Pop** removes and displays the top value.
- **Peek** highlights the top value without removing it.
- **Clear** empties the stack and removed-items display.

## Queue Simulator

From the `queue-simulator` folder:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5001`.

Supported operations:

- **Enqueue** adds a value to the rear of the queue.
- **Dequeue** removes and displays the front value.
- **Peek** highlights the front value without removing it.
- **Clear** empties the queue and removed-items display.

Both applications store their state in Flask sessions and use Jinja templates with Bootstrap, custom CSS, jQuery, flash messages, and template inheritance.
