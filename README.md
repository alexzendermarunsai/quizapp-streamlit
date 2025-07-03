# CompTIA Pentest+ PT0-003 Quiz App

## Introduction

Welcome to the CompTIA Pentest+ PT0-003 Quiz App! This application is designed to help you prepare for the CompTIA PenTest+ (PT0-003) certification exam. It provides a platform to test your knowledge on various topics covered in the exam through a series of quiz questions, including multiple-choice and simulation-based scenarios.

This tool is ideal for:
- Individuals preparing for the CompTIA PenTest+ (PT0-003) exam.
- Cybersecurity professionals looking to refresh their penetration testing knowledge.
- Students and enthusiasts interested in learning more about offensive security concepts.

The quiz app leverages a question bank in JSON format (`questions_bank.json`) and presents questions in a user-friendly interface powered by Streamlit.

## How to Use

This application is run as a Streamlit app. Ensure you have Python and Streamlit installed.

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run streamlit_app.py
    ```
    The application will open in your default web browser.

### Navigating the App

-   **Main Area:** Displays the current question or the final results.
-   **Sidebar:**
    -   **CONTROLS:**
        -   `🔄 RESET SESSION`: Click this button to clear your current progress (score, answers, current question) and start the quiz from the beginning. The question bank will be reloaded.
    -   **STATUS:**
        -   Shows your current `SCORE` (number of correct answers out of the total questions attempted so far).
        -   A progress bar indicates how far you are through the quiz.
        -   Displays the current question number you are on (`Analyzing Target: X / Y`).
    -   **Navigation:**
        -   `Enter question number to jump to:`: Input a question number and click "Go to Question" to directly navigate to that specific question.

### Answering Questions

The app presents different types of questions:

-   **Multiple Choice (Single Answer):** Indicated by radio buttons. Select one option.
-   **Multiple Choice (Multiple Answers - Exactly Two):** Indicated by checkboxes. You must select exactly two options.
-   **Multiple Choice (Multiple Answers - All Applicable):** Indicated by a multiselect dropdown. Select one or more options.
-   **Simulation Scenarios:** These questions present a scenario and may provide details in a text area. There isn't a direct "answer" to submit; you review the information and proceed.

**Submitting Answers:**
-   For multiple-choice questions, after making your selection(s), click the **"EXECUTE"** button.
-   The app will immediately tell you if your answer was correct (`✅ ACCESS GRANTED`) or incorrect (`❌ ACCESS DENIED`).
-   The correct answer(s) will be shown.
-   An **"/// DEBRIEF ///"** section will appear below the feedback, providing an explanation for the question and why the correct answer is what it is.

**Navigating Through Questions:**
-   **`⬅️ PREVIOUS`**: Moves to the previous question. This button is disabled if you are on the first question or if you haven't answered the current question (for non-simulation types).
-   **`NEXT ➡️`** (or **`NEXT SIM/TARGET ➡️`** for simulations): Moves to the next question.
    -   For multiple-choice questions, this button is typically disabled until you submit an answer via "EXECUTE".
    -   For simulations, you can proceed to the next target/question using this button. If you move past a simulation without "answering" (as there's no explicit submission), it will be marked as bypassed in the final report.
-   When you reach the end of the quiz, the "NEXT" button will change to **`VIEW REPORT 🏁`**.

### Reviewing Results

-   After completing all questions and clicking "VIEW REPORT 🏁", you'll see the **"🏁 MISSION COMPLETE 🏁"** page.
-   Your **Final Score** and percentage will be displayed.
-   Below this, the **"/// ANALYSIS RESULTS ///"** section provides an expandable summary for each question:
    -   Click on a question summary (e.g., "Target 1 (#REF_ID): Question text snippet...") to expand it.
    -   You'll see the full question text.
    -   **Your Response:** What you submitted.
    -   **Correct Response:** The actual correct answer(s).
    -   Feedback on whether you were correct or not.
    -   The **"/// DEBRIEF ///"** (explanation) for that question.
    -   For simulations, it will indicate if they were bypassed.

### Question Bank

The questions are loaded from `questions_bank.json`. You can customize this file to add, remove, or modify questions. Ensure the JSON structure is maintained for the app to function correctly.

## Contributing

Contributions are welcome! If you'd like to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Ensure your changes are well-tested (if applicable).
5. Add or update questions in `questions_bank.json` following the existing format.
6. Create a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.