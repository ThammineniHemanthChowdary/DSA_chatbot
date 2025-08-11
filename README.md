# 🧠 DSA Study Buddy

An **AI-powered study chatbot** for learning and practicing **Data Structures & Algorithms (DSA)** in a beginner-friendly way.

This tool helps you:

- 📚 Learn DSA concepts with **simple explanations**.
- 📝 Load coding problems from a local problem bank.
- 💡 Get **progressive hints** using a Hugging Face model (1 = small nudge, 4 = pseudocode).
- ⌨️ Write and test your own solutions directly in the browser.
- ✅ See **pass/fail results**, runtime, peak memory usage, and **complexity analysis**.
- 📊 Visualize empirical runtime vs. input size.
- 📈 *(Future)* Track progress, maintain streaks, and focus on weak topics with spaced repetition.

---

## 🚀 Features

- **Gradio web UI** for interactive problem-solving.
- **Hugging Face API** for AI-generated hints.
- **Safe code execution** with restrictions on dangerous imports/functions.
- **Automatic complexity analysis**:
  - 📄 Static AST-based time complexity guess.
  - ⚡ Empirical benchmarking with plotted runtime.
- **Modular architecture**:
  - `core/` — logic (problems, hints, runner, complexity).
  - `data/` — problems and concept notes.

---

## 📂 Project Structure

.
├── app.py # Main Gradio app
├── core/
│ ├── init.py
│ ├── problems.py # Problem loading
│ ├── hints.py # AI hint generation
│ ├── runner.py # Safe code execution
│ ├── complexity.py # Complexity analysis
│ └── progress.py # (Future) Progress tracking
├── data/
│ ├── problems/ # Problem JSON files
│ └── concepts/ # Short concept explanations
├── requirements.txt
├── .gitignore
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/<your-username>/DSA_chatbot.git
cd DSA_chatbot

2️⃣ Create a virtual environment & install dependencies
python -m venv .venv

# Activate the environment
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

3️⃣ Configure environment variables
Create a .env file in the project root:
HF_API_TOKEN=hf_your_huggingface_token_here
HINT_MODEL=mistralai/Mistral-7B-Instruct-v0.3

▶️ Running the App
python app.py

📌 Usage Flow
Select a problem from the dropdown and click Load Problem.

Read the title, function signature, and sample input/output.

Use Get Hint to get progressive help from the AI.

Write your solution in the code editor.

Click Run & Test to check against sample and hidden cases.

View results, performance metrics, complexity analysis, and runtime plot.

🛠️ Future Improvements
Step 6: Progress tracking with SQLite (streaks & spaced repetition)

More problems and concept explanations

Support for multiple programming languages

Deploy to Hugging Face Spaces for public access

📜 License
MIT License

🙌 Acknowledgments
Gradio for the interactive UI

Hugging Face for model inference

Python standard libraries for safe code execution & profiling


