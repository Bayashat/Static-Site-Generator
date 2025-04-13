# 🛠 Static Site Generator in Python

Welcome to my very own **Static Site Generator**, built from scratch in Python.  
It transforms Markdown files into a fully functional static website using only standard libraries — no frameworks or external dependencies.

---

## 🚀 Features

- 🧱 Converts `.md` files to clean HTML pages  
- 📂 Recursively supports nested directories (e.g., `/blog/tom/index.md`)  
- 🔗 Parses inline Markdown elements: bold, italics, links  
- 🖼 Utilizes a reusable HTML template (`template.html`)  
- 🧪 Includes automated test scripts  
- 🧵 Modular codebase using clean Python packaging

---

## 🔧 Project Structure

```plaintext
scripts/
├── main.sh          # Bash entrypoint to run the site generator locally
├── test.sh          # Run unit tests
├── build.sh         # Bash script to build the site

src/                 # Source code for the site generator
content/             # Markdown content source (input)
docs/                # Generated HTML output (final site)
template.html        # Reusable HTML template
```

---

## 🖼️ Architecture Overview
![Architecture](static/images/architecture.png)


## 📈 How to Use
```bash
# Step 1: Build the site from Markdown
./scripts/build.sh

# Or directly with Python (from project root):
python3 -m src.generator.main.py

# Step 2: Open the generated site
```

## ✅ To-Do
- [ ] Add support for nested inline elements (e.g., bold inside italics)
- [ ] Implement CLI arguments for input/output directory
- [ ] Add support for Markdown images

## 🤓 What I Learned
* ✅ This project deepened my understanding of:
* ✅ Recursive directory traversal
* ✅ Markdown parsing logic
* ✅ HTML templating in Python
* ✅ Modular software design using OOP

---

> If you'd like to try it out or contribute, feel free to fork this repo or drop a ⭐ on GitHub!