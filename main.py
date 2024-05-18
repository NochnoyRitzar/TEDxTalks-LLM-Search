import streamlit as st

def process_query(query):
    # Placeholder function to process the query
    # Replace this with actual logic to find TED talks
    return [
        {"title": "Talk 1", "speaker": "Speaker 1", "description": "Description of talk 1"},
        {"title": "Talk 2", "speaker": "Speaker 2", "description": "Description of talk 2"},
        {"title": "Talk 3", "speaker": "Speaker 3", "description": "Description of talk 3"},
        {"title": "Talk 4", "speaker": "Speaker 4", "description": "Description of talk 4"},
    ]

def display_cards(talks):
    # Create a grid of cards to display the talks
    cols = st.columns(4)
    for col, talk in zip(cols, talks):
        with col:
            st.subheader(talk['title'])
            st.write(f"Speaker: {talk['speaker']}")
            st.write(talk['description'])

def main():
    st.title('TED Talk Finder')
    user_query = st.text_input("Enter your query to find the best TED talks:", "")

    if user_query:
        # Process the query to get TED talks
        result_talks = process_query(user_query)
        # Display the talks in cards
        display_cards(result_talks)

if __name__ == "__main__":
    main()
