import streamlit.components.v1 as components
import os

# Create a function _component_func which will call the frontend component when run
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
component_func = components.declare_component("highlightable_text", path=build_dir)
_component_func = components.declare_component(
    "highlightable_text",
    path="component/frontend/build",  # Fetch frontend component from local webserver
)

# Define a public function for the package,
# which wraps the caller to the frontend code
def highlightable_text(data):
    
    component_value = _component_func(data=data)
    return component_value

