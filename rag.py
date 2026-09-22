"""
Simple local design knowledge retrieval system.

This version keeps the project lightweight and easy to deploy
on Streamlit Community Cloud.

It can later be upgraded to FAISS or another vector database.
"""


DESIGN_KNOWLEDGE = [

    {
        "topic": "space planning",

        "text": (
            "Maintain clear circulation paths and avoid blocking "
            "doors, windows, wardrobes, or major furniture access. "
            "Furniture placement should be checked against the "
            "dimensions supplied by the user."
        )
    },

    {
        "topic": "lighting",

        "text": (
            "A practical residential lighting plan can combine "
            "ambient lighting, task lighting for activities such "
            "as reading or studying, and accent lighting where "
            "useful."
        )
    },

    {
        "topic": "storage",

        "text": (
            "Use vertical storage, under-bed storage, "
            "multifunctional furniture, and wall-mounted solutions "
            "where appropriate, while preserving usable circulation."
        )
    },

    {
        "topic": "color",

        "text": (
            "Lighter colors can help a small room feel visually "
            "more open. Accent colors can be concentrated on one "
            "wall, textiles, artwork, or small decor elements."
        )
    },

    {
        "topic": "budget",

        "text": (
            "Budget planning should distinguish between furniture, "
            "lighting, storage, decor, installation, and a "
            "contingency allowance. Actual local prices should be "
            "verified before purchase."
        )
    }

]


def retrieve_knowledge(room_data, top_k=5):

    query = " ".join(
        str(value)
        for value in room_data.values()
    ).lower()

    scored_items = []

    for item in DESIGN_KNOWLEDGE:

        searchable_text = (
            item["topic"] + " " + item["text"]
        ).lower()

        terms = searchable_text.split()

        score = sum(
            1
            for term in terms
            if len(term) > 3 and term in query
        )

        scored_items.append(
            (score, item)
        )

    # Highest relevance first
    scored_items.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected_items = [

        item

        for score, item in scored_items[:top_k]

        if score > 0

    ]

    # If no matching information was found,
    # provide general design knowledge.
    if not selected_items:

        selected_items = DESIGN_KNOWLEDGE[:top_k]

    return "\n".join(

        f"- {item['topic'].title()}: {item['text']}"

        for item in selected_items

    )
