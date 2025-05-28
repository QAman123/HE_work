import streamlit as st
import json

import streamlit.components.v1 as components

# Hide Streamlit branding, menu, and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



def scroll_to_top():
    components.html(
        """
        <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
        """,
        height=0,
    )



# Load tree
with open("decision_tree_test.json") as f:
    tree = json.load(f)

# Initialize session state
if "path" not in st.session_state:
    # Each entry: (node_key, chosen_option, main_question)
    st.session_state.path = []

if "node" not in st.session_state:
    st.session_state.node = "start"

def go_to_node(node_key, path_index=None):
    """Jump to a node and optionally truncate path."""
    st.session_state.node = node_key
    if path_index is not None:
        st.session_state.path = st.session_state.path[:path_index]
    st.rerun()

# Sidebar: show history with clickable main questions + chosen answer
st.sidebar.title("Decisions made")
for i, (node_key, chosen_option, main_q) in enumerate(st.session_state.path):
    if st.sidebar.button(f"{i+1}. {main_q}", key=f"path_{i}"):
        go_to_node(node_key, path_index=i)
    st.sidebar.markdown(f"&nbsp;&nbsp;&nbsp;➡️ *You chose:* **{chosen_option}**", unsafe_allow_html=True)

# Current node data
node = tree[st.session_state.node]

# Split main question and details (expect main question on first line, details after)
text_lines = node["text"].split('\n', 1)
main_question = text_lines[0] if len(text_lines) > 0 else ""
details = text_lines[1] if len(text_lines) > 1 else ""

# Display question
st.title(main_question)                   # Bold + bigger font by default with title
if details.strip():
    st.markdown(details)                  # Formatted markdown for details


# Optional image
if "image2" in node:
    st.image(node["image2"], use_container_width=True)


# Final advice node
if node.get("advice"):
    st.success(node.get("advice_text", "You have reached an outcome."))
    st.markdown("---")  # or st.write("") for a blank line

    if st.button("♻️ *Start Over* ♻️"):
        st.session_state.node = "start"
        st.session_state.path = []
        st.rerun()



else:
    # Show option buttons
    st.markdown("---")  # or st.write("") for a blank line
    for option, next_node in node["options"].items():
        if st.button(option):
            # Append to path: (current node, chosen option, main question)
            st.session_state.path.append((st.session_state.node, option, main_question))
            st.session_state.node = next_node
            st.rerun()
    st.markdown("---")  # or st.write("") for a blank line

# Show back button
if st.session_state.path:
    if st.button("↩️ *Go back 1 step* ↩️"):
        last_node_key, _, _ = st.session_state.path[-1]
        st.session_state.node = last_node_key
        st.session_state.path = st.session_state.path[:-1]
        st.rerun()

# Optional image
if "image" in node:
    st.image(node["image"], use_container_width=True)