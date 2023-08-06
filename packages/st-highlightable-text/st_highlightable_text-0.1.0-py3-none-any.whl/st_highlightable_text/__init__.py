import streamlit.components.v1 as components
import os

_RELEASE = True

if (_RELEASE):
# Create a function _component_func which will call the frontend component when run
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    print(build_dir)
    _component_func = components.declare_component("highlightable_text", path=build_dir)


else:
    _component_func = components.declare_component("highlightable_text", url="http://localhost:3001")

# Define a public function for the package,
# which wraps the caller to the frontend code
def highlightable_text(data):
    component_value = _component_func(data=data)
    return component_value

