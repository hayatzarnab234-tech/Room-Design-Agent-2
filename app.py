import streamlit as st
from agent import generate_room_design

st.set_page_config(
    page_title="Room Design Agent",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Room Design Agent")
st.write(
    "Create a practical residential room-design plan based on "
    "your space, budget, style, and requirements."
)

st.divider()

# -----------------------------
# User Inputs
# -----------------------------

st.header("Room Information")

col1, col2 = st.columns(2)

with col1:
    room_type = st.text_input(
        "Room Type",
        placeholder="e.g. Bedroom, Living Room, Study Room"
    )

    dimensions = st.text_input(
        "Room Dimensions",
        placeholder="e.g. 12 ft × 14 ft"
    )

    budget = st.text_input(
        "Budget",
        placeholder="e.g. PKR 150,000"
    )

    design_style = st.text_input(
        "Preferred Design Style",
        placeholder="e.g. Modern Minimalist"
    )

with col2:
    colors = st.text_input(
        "Preferred Colors",
        placeholder="e.g. Beige, White, Sage Green"
    )

    furniture = st.text_area(
        "Required Furniture",
        placeholder="e.g. Queen bed, wardrobe, study desk, chair"
    )

    functional_requirements = st.text_area(
        "Functional Requirements",
        placeholder="e.g. Good storage, study area, open walking space"
    )

    additional_preferences = st.text_area(
        "Additional Preferences",
        placeholder="Anything else you want the agent to consider"
    )

st.divider()

# -----------------------------
# Generate Design
# -----------------------------

if st.button(
    "✨ Generate Room Design",
    type="primary",
    use_container_width=True
):

    missing_information = []

    if not room_type.strip():
        missing_information.append("Room Type")

    if not dimensions.strip():
        missing_information.append("Room Dimensions")

    if not budget.strip():
        missing_information.append("Budget")

    if missing_information:
        st.warning(
            "Please provide the following required information: "
            + ", ".join(missing_information)
        )

    else:

        room_data = {
            "room_type": room_type,
            "dimensions": dimensions,
            "budget": budget,
            "style": design_style,
            "colors": colors,
            "furniture": furniture,
            "functional_requirements": functional_requirements,
            "additional_preferences": additional_preferences
        }

        with st.spinner("Designing your room..."):

            try:

                result = generate_room_design(room_data)

                st.success("Room design generated successfully!")

                st.markdown(result)

            except Exception as error:

                st.error(
                    "The room design could not be generated."
                )

                st.exception(error)


st.divider()

st.caption(
    "Room Design Agent • Gemini-powered residential interior design assistant"
)
