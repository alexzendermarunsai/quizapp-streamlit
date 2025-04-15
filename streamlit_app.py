import streamlit as st
import json
import os

# --- Configuration ---
JSON_FILE = 'questions_bank.json'

# --- Functions ---
# ... (load_questions, initialize_state, reset_quiz, parse_correct_answer functions remain the same) ...
@st.cache_data # Cache the data loading
def load_questions(filename):
    """Loads quiz questions from the JSON file."""
    if not os.path.exists(filename) or not os.path.isfile(filename):
        st.error(f"Error: Questions file '{filename}' not found.")
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        if not isinstance(questions_data, list):
             st.error(f"Error: Questions file '{filename}' does not contain a valid JSON list.")
             return None

        validated_questions = []
        for i, q in enumerate(questions_data):
             if not isinstance(q, dict):
                 st.warning(f"Warning: Item at index {i} in '{filename}' is not a dictionary. Skipping.")
                 continue
             is_sim = q.get('is_simulation', False)
             if 'question_text' not in q:
                  st.warning(f"Warning: Question index {i} missing 'question_text'. Skipping.")
                  continue
             # Validation for non-simulation questions
             if not is_sim:
                  if ('options' not in q or q.get('options') is None or not isinstance(q.get('options'), dict)):
                      st.warning(f"Warning: Non-simulation Q{i} missing valid 'options'. Skipping.")
                      continue
                  if ('correct_answer' not in q):
                      st.warning(f"Warning: Non-simulation Q{i} missing 'correct_answer' key. Skipping.")
                      continue
                  ca = q.get('correct_answer')
                  if isinstance(ca, str) and not ca.strip():
                      st.warning(f"Warning: Non-simulation Q{i} has an empty string for 'correct_answer'. Skipping.")
                      continue
                  if isinstance(ca, str):
                      keys_in_ca = [k for k in ca.strip().split(' ') if k]
                      valid_options = q.get('options', {})
                      if not all(k in valid_options for k in keys_in_ca):
                           st.warning(f"Warning: Non-simulation Q{i} has 'correct_answer' keys ('{ca}') not present in its 'options'. Skipping.")
                           continue
             validated_questions.append(q)

        if not validated_questions:
             st.error(f"Error: No valid questions found in '{filename}' after validation.")
             return None
        return validated_questions
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON from '{filename}': {e}. Please ensure it's valid JSON.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading '{filename}': {e}")
        return None

def initialize_state():
    """Initializes session state variables."""
    if 'current_question_index' not in st.session_state: st.session_state.current_question_index = 0
    if 'score' not in st.session_state: st.session_state.score = 0
    if 'results' not in st.session_state: st.session_state.results = {}
    if 'questions' not in st.session_state: st.session_state.questions = None
    if 'total_questions' not in st.session_state: st.session_state.total_questions = 0
    if 'navigated' not in st.session_state: st.session_state.navigated = False

def reset_quiz():
    """Resets the quiz state."""
    keys_to_reset = ['current_question_index', 'score', 'results', 'questions', 'total_questions', 'navigated']
    for key in keys_to_reset:
        if key in st.session_state: del st.session_state[key]
    load_questions.clear()
    initialize_state()
    st.rerun()

def parse_correct_answer(correct_answer_value):
    """Parses the correct_answer string into a sorted list of keys."""
    if isinstance(correct_answer_value, str):
        keys = sorted([key for key in correct_answer_value.strip().split(' ') if key])
        return keys
    return []

# --- Inject Custom CSS (REMOVED fixed nav styles, kept theme styles) <<< CHANGE >>> ---
st.markdown("""
    <style>
        /* Ensure monospace font is applied widely */
        html, body, [class*="st-"], .main * {
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        }

        /* Style buttons */
        .stButton > button {
            border: 1px solid #00ff41; /* Green border */
            border-radius: 0; /* Square corners */
            background-color: #1a1a1a; /* Dark background */
            color: #00ff41; /* Green text */
            padding: 8px 15px;
            transition: all 0.3s ease;
            box-shadow: 0 0 5px rgba(0, 255, 65, 0.3); /* Subtle green glow */
        }
        .stButton > button:hover {
            background-color: #00ff41; /* Green background on hover */
            color: #0a0a0a; /* Dark text on hover */
            border-color: #00ff41;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.7); /* Brighter glow */
        }
        .stButton > button:disabled {
            border-color: #555;
            background-color: #222;
            color: #555;
            opacity: 0.7;
            box-shadow: none;
        }

        /* Style feedback boxes (Success/Error/Info/Warning) */
        .stAlert {
            border-radius: 0 !important;
            border-left: 5px solid !important;
            background-color: #1a1a1a !important;
        }
        .stAlert[data-baseweb="notification"][data-kind="success"] { border-left-color: #00ff41 !important; color: #00ff41 !important; }
        .stAlert[data-baseweb="notification"][data-kind="error"] { border-left-color: #ff4757 !important; color: #ff4757 !important; }
        .stAlert[data-baseweb="notification"][data-kind="warning"] { border-left-color: #ffa502 !important; color: #ffa502 !important; }
        .stAlert[data-baseweb="notification"][data-kind="info"] { border-left-color: #00ffff !important; color: #00ffff !important; }
        .stAlert svg { fill: currentColor !important; }

        /* Style expanders */
        .stExpander { border: 1px solid #555 !important; border-radius: 0 !important; background-color: #1a1a1a !important; }
        .stExpander header { font-size: 1.1em !important; color: #00ff41 !important; background-color: #1a1a1a !important; }

        /* Style progress bar */
        .stProgress > div > div > div > div { background-color: #00ff41 !important; }

        /* Style radio/checkbox labels */
        label[data-baseweb="radio"] span, label[data-baseweb="checkbox"] span { color: #e0e0e0 !important; }
        label[data-baseweb="radio"] span:hover, label[data-baseweb="checkbox"] span:hover { color: #00ff41 !important; }

        /* Style the multiselect dropdown */
        div[data-baseweb="select"] > div { background-color: #1a1a1a !important; border: 1px solid #555 !important; border-radius: 0 !important; color: #e0e0e0 !important; }
        /* Style multiselect pills */
        span[data-baseweb="tag"] { background-color: #00ff41 !important; color: #0a0a0a !important; border-radius: 0 !important; }

        /* REMOVED: .fixed-bottom-nav styles */
        /* REMOVED: padding-bottom style for main container */

    </style>
""", unsafe_allow_html=True)

# --- Main App Logic ---
initialize_state()

# --- Load Questions ---
if st.session_state.questions is None:
    with st.spinner("Establishing connection... Loading question bank..."):
        st.session_state.questions = load_questions(JSON_FILE)
    if st.session_state.questions:
        st.session_state.total_questions = len(st.session_state.questions)
    else:
        st.error("FATAL ERROR: Cannot load question bank. Aborting operation.")
        st.stop()

questions = st.session_state.questions
total_questions = st.session_state.total_questions
current_index = st.session_state.current_question_index
score = st.session_state.score
results = st.session_state.results

if total_questions == 0:
    st.error("ERROR: No valid questions found in source.")
    if st.button("🔄 Attempt Re-init"):
        reset_quiz()
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.header("Pentester+ Quiz Interface v0.3")
    st.divider()
    st.header("CONTROLS")
    if st.button("🔄 RESET SESSION"):
        reset_quiz()
    st.header("STATUS")
    st.write(f"SCORE: {score} / {total_questions}")
    progress_percent = ((current_index + 1) / total_questions) if total_questions > 0 else 0
    progress_percent = max(0.0, min(1.0, progress_percent))
    st.progress(progress_percent)
    if current_index >= total_questions: st.write(">> Scan Complete <<")
    else: st.write(f">> Analyzing Target: {current_index + 1} / {total_questions}")

# --- Main Content Area ---

# Scroll logic
if st.session_state.get("navigated", False):
    st.components.v1.html("<script>window.parent.document.body.scrollTop = 0;</script>", height=0)
    st.session_state.navigated = False

# 1. Results Page
if current_index >= total_questions:
    st.header("🏁 MISSION COMPLETE 🏁")
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    st.metric(label="Final Score", value=f"{score} / {total_questions}", delta=f"{percentage:.1f}%")
    st.subheader("/// ANALYSIS RESULTS ///")
    if not results:
        st.info(">>> No engagement data recorded. <<<")
    else:
        # ... (Results review logic remains the same) ...
        for i in range(total_questions):
            if i >= len(questions): continue
            question_data = questions[i]
            q_num_ref = f" (#{question_data.get('question_number', 'N/A')})"
            q_text_snippet = question_data.get('question_text', '[No Text]')[:80] + "..."
            with st.expander(f"Target {i+1}{q_num_ref}: {q_text_snippet}", expanded=False):
                st.markdown(f"**{question_data.get('question_text', '[No Text]')}**")
                result_data = results.get(i)
                original_correct_answer = question_data.get('correct_answer')

                if question_data.get('is_simulation', False):
                    st.info("Type: Simulation Scenario")
                    if result_data and result_data.get('submitted'):
                         st.write(f"Status: {result_data.get('submitted', '[ bypassed ]')}")
                    if 'simulation_details' in question_data:
                        st.text_area("Simulation Parameters:", question_data['simulation_details'], height=100, disabled=True, key=f"review_sim_{i}")
                elif result_data:
                    submitted = result_data.get('submitted', '[ No Response ]')
                    is_correct = result_data.get('correct', False)
                    explanation = question_data.get('explanation', '/// No Debrief Available ///')
                    submitted_display = ', '.join(sorted(submitted)) if isinstance(submitted, list) else submitted
                    if not submitted_display: submitted_display = "[ No Response ]"
                    st.write(f"Your Response: `{submitted_display}`")
                    st.write(f"Correct Response: `{original_correct_answer or 'N/A'}`")
                    if is_correct: st.success("✅ ACCESS GRANTED")
                    else: st.error("❌ ACCESS DENIED")
                    st.markdown("**Debrief:**")
                    st.info(explanation)
                else:
                    st.warning("⚠️ TARGET SKIPPED")
                    st.write(f"Correct Response: `{original_correct_answer or 'N/A'}`")

    # --- Navigation on Results Page (NOT Wrapped) <<< CHANGE >>> ---
    # REMOVED st.markdown('<div class="fixed-bottom-nav">', unsafe_allow_html=True)
    if st.button("⬅️ REVIEW PREVIOUS", disabled=(current_index <= 0)):
        st.session_state.current_question_index -= 1
        st.session_state.navigated = True
        st.rerun()
    # REMOVED st.markdown('</div>', unsafe_allow_html=True)

# 2. Question Display
else:
    # ... (Error checking and question type determination logic remains the same) ...
    if current_index < 0 or current_index >= len(questions):
         st.error(f"CRITICAL ERROR: Invalid index ({current_index}). Resetting session.")
         reset_quiz()
         st.stop()

    current_question = questions[current_index]
    is_simulation = current_question.get('is_simulation', False)
    options = current_question.get('options', {})
    correct_answer_str = current_question.get('correct_answer')

    question_type = 'simulation'
    num_correct_keys = 0
    correct_answer_keys = []
    if not is_simulation:
        if isinstance(correct_answer_str, str) and correct_answer_str.strip():
            correct_answer_keys = parse_correct_answer(correct_answer_str)
            num_correct_keys = len(correct_answer_keys)
            if num_correct_keys == 1: question_type = 'radio'
            elif num_correct_keys == 2: question_type = 'checkbox'
            elif num_correct_keys > 2: question_type = 'multiselect'
            else:
                 st.warning(f"Target {current_index+1}: Config error ('{correct_answer_str}'). Simulating.", icon="⚠️")
                 question_type = 'simulation'; is_simulation = True
        else:
            st.warning(f"Target {current_index+1}: Missing/invalid config. Simulating.", icon="⚠️")
            question_type = 'simulation'; is_simulation = True

    has_been_answered = current_index in results

    st.subheader(f"{'// SIMULATION //' if is_simulation else '// QUESTION //'} {current_index + 1} / {total_questions}")
    q_num_ref = current_question.get('question_number')
    if q_num_ref: st.caption(f"Ref ID: {q_num_ref}")

    # --- Form for answering ---
    with st.form(key=f"quiz_form_{current_index}", clear_on_submit=False):
        st.markdown(f"**>>> {current_question.get('question_text', 'Text segment corrupted.')}**")

        # --- Render Widgets ---
        # ... (Widget rendering logic remains the same) ...
        if question_type == 'simulation':
            st.info("Analyze parameters and proceed.")
            if current_question.get('simulation_details'): st.text_area("Parameters:", current_question['simulation_details'], height=150, disabled=True, key=f"sim_details_{current_index}")
        elif question_type == 'checkbox':
            st.markdown("**Select EXACTLY TWO responses:**")
            for opt_key, opt_text in options.items():
                default_checked = has_been_answered and isinstance(results[current_index].get('submitted'), list) and opt_key in results[current_index]['submitted']
                st.checkbox(f"[{opt_key}] {opt_text}", key=f"q_{current_index}_option_{opt_key}", value=default_checked, disabled=has_been_answered)
        elif question_type == 'multiselect':
            st.markdown("**Select ALL applicable responses:**")
            display_options_multi = {f"[{k}] {v}": k for k, v in options.items()}
            option_keys_ordered_multi = list(display_options_multi.keys())
            default_selection_multi = []
            if has_been_answered and isinstance(results[current_index].get('submitted'), list):
                submitted_keys = results[current_index]['submitted']
                default_selection_multi = [disp for disp, k in display_options_multi.items() if k in submitted_keys]
            st.multiselect("Input:", option_keys_ordered_multi, default=default_selection_multi, key=f"q_{current_index}_multiselect_value", disabled=has_been_answered)
        elif question_type == 'radio':
            st.markdown("**Select ONE response:**")
            display_options_radio = {f"[{k}] {v}": k for k, v in options.items()}
            option_keys_ordered_radio = list(display_options_radio.keys())
            default_index_radio = None
            if has_been_answered and isinstance(results[current_index].get('submitted'), str):
                submitted_key = results[current_index]['submitted']
                matching_display = [disp for disp, k in display_options_radio.items() if k == submitted_key]
                if matching_display:
                    try: default_index_radio = option_keys_ordered_radio.index(matching_display[0])
                    except ValueError: pass
            st.radio("Input:", option_keys_ordered_radio, index=default_index_radio, key=f"q_{current_index}_radio_value", disabled=has_been_answered, format_func=lambda x: x)

        # --- Submit Button (Inside Form) ---
        submit_button_label = "EXECUTE"
        disable_submit = has_been_answered or (question_type == 'simulation')
        submitted_via_button = st.form_submit_button(submit_button_label, disabled=disable_submit)

        # --- Process Submission (Inside Form) ---
        if submitted_via_button and question_type != 'simulation' and not has_been_answered:
            # ... (Submission processing logic remains the same) ...
            actual_submitted_answer = None
            is_valid_submission = False
            if question_type == 'checkbox':
                collected_keys = [opt_key for opt_key in options if st.session_state.get(f"q_{current_index}_option_{opt_key}", False)]
                actual_submitted_answer = sorted(collected_keys)
                if len(actual_submitted_answer) == 2: is_valid_submission = True
                else: st.warning("Input Error: Requires exactly 2 selections.", icon="⚠️")
            elif question_type == 'multiselect':
                widget_key_multi = f"q_{current_index}_multiselect_value"
                selected_display_values = st.session_state.get(widget_key_multi, [])
                display_options_multi_map = {f"[{k}] {v}": k for k, v in options.items()}
                collected_keys = [display_options_multi_map[val] for val in selected_display_values if val in display_options_multi_map]
                actual_submitted_answer = sorted(collected_keys)
                if actual_submitted_answer: is_valid_submission = True
                else: st.warning("Input Error: Requires at least 1 selection.", icon="⚠️")
            elif question_type == 'radio':
                widget_key_radio = f"q_{current_index}_radio_value"
                selected_display_value = st.session_state.get(widget_key_radio, None)
                display_options_radio_map = {f"[{k}] {v}": k for k, v in options.items()}
                actual_submitted_answer = display_options_radio_map.get(selected_display_value)
                if actual_submitted_answer is not None: is_valid_submission = True
                else: st.warning("Input Error: Requires 1 selection.", icon="⚠️")

            if is_valid_submission:
                 submitted_answer_norm = actual_submitted_answer if isinstance(actual_submitted_answer, list) else [actual_submitted_answer]
                 is_correct = (submitted_answer_norm == correct_answer_keys)
                 if is_correct: st.session_state.score += 1
                 st.session_state.results[current_index] = {'submitted': actual_submitted_answer, 'correct': is_correct, 'is_simulation': False, 'question_type': question_type}
                 st.rerun()

    # --- FORM END ---

    # --- Display Feedback (Outside Form) ---
    if not is_simulation and has_been_answered:
        # ... (Feedback display logic remains the same) ...
        result = results[current_index]
        submitted = result.get('submitted')
        explanation = current_question.get('explanation', '/// No Debrief Available ///')
        is_correct = result.get('correct')
        original_correct_answer = current_question.get('correct_answer')
        submitted_display = ', '.join(sorted(submitted)) if isinstance(submitted, list) else submitted
        if not submitted_display: submitted_display = "[ No Response ]"
        if is_correct: st.success(f"✅ ACCESS GRANTED | Your input: `{submitted_display}`")
        else: st.error(f"❌ ACCESS DENIED | Your input: `{submitted_display}`, Expected: `{original_correct_answer}`")
        st.markdown("**Debrief:**")
        st.info(explanation)

    # --- Navigation Buttons (NOT Wrapped) <<< CHANGE >>> ---
    st.write("---") # Add a separator before nav buttons
    # REMOVED st.markdown('<div class="fixed-bottom-nav">', unsafe_allow_html=True)
    nav_cols = st.columns(2)
    with nav_cols[0]: # Previous
        if st.button("⬅️ PREVIOUS", disabled=(current_index <= 0), key="nav_prev"):
            st.session_state.current_question_index -= 1
            st.session_state.navigated = True
            st.rerun()
    with nav_cols[1]: # Next
        next_label = "NEXT ➡️"
        if question_type == 'simulation': next_label = "NEXT SIM/TARGET ➡️"
        if current_index == total_questions - 1: next_label = "VIEW REPORT 🏁"
        disable_next = (question_type != 'simulation') and not has_been_answered
        if st.button(next_label, disabled=disable_next, key="nav_next"):
            if question_type == 'simulation' and current_index not in results:
                 st.session_state.results[current_index] = {'submitted': '[Simulation Bypassed]', 'correct': None, 'is_simulation': True, 'question_type': 'simulation'}
            st.session_state.current_question_index += 1
            st.session_state.navigated = True
            st.rerun()
    # REMOVED st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
# Restore footer if desired
st.markdown("---")
st.caption("Interface Active.")