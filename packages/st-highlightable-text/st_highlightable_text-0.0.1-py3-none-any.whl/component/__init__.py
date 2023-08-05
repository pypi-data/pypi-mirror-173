import streamlit.components.v1 as components

# Create a function _component_func which will call the frontend component when run
_component_func = components.declare_component(
    "highlightable_text",
    path="component/frontend/build",  # Fetch frontend component from local webserver
)

# Define a public function for the package,
# which wraps the caller to the frontend code
def highlightable_text(data):
    component_value = _component_func(data=data)
    return component_value

