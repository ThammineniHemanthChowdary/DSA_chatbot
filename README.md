🧠 DSA Study Buddy
An AI-powered study chatbot for learning and practicing Data Structures & Algorithms (DSA) in a beginner-friendly way.

This tool lets you:

Learn DSA concepts with simple explanations.

Load coding problems from a local problem bank.

Get progressive hints using a Hugging Face model (1 = small nudge, 4 = pseudocode).

Write and test your own solutions directly in the browser.

See pass/fail results, runtime, peak memory usage, and complexity analysis (O-notation).

Visualize empirical runtime vs. input size.

(Future) Track progress, maintain streaks, and use spaced repetition to focus on weak topics.

🚀 Features
Gradio web UI for interactive problem-solving.

Hugging Face API for AI-generated hints.

Safe code execution with restrictions on dangerous imports/functions.

Automatic time & space complexity analysis:

Static AST-based guess.

Empirical benchmarking with plotted runtime.

Modular architecture:

core/ for logic (problems, hints, runner, complexity)

data/ for problems and concept notes

📂 Project Structure
bash
Copy
Edit
.
├── app.py               # Main Gradio app
├── core/
│   ├── __init__.py
│   ├── problems.py      # Problem loading
│   ├── hints.py         # AI hint generation
│   ├── runner.py        # Safe code execution
│   ├── complexity.py    # Complexity analysis
│   └── progress.py      # (Future) Progress tracking
├── data/
│   ├── problems/        # Problem JSON files
│   └── concepts/        # Short concept explanations
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the repo
bash
Copy
Edit
git clone https://github.com/<your-username>/DSA_chatbot.git
cd DSA_chatbot
2️⃣ Create a virtual environment & install dependencies
bash
Copy
Edit
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

ini
Copy
Edit
HF_API_TOKEN=hf_your_huggingface_token_here
HINT_MODEL=mistralai/Mistral-7B-Instruct-v0.3
▶️ Running the App
bash
Copy
Edit
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

