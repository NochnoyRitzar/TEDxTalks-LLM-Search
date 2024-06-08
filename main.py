import streamlit as st
from dotenv import load_dotenv
from src.pinecone_utils import create_pinecone_retriever

load_dotenv(".env")
retriever = create_pinecone_retriever(top_k=3)


def retrieve_similar_talks(query):
    results = retriever.retrieve(query)

    response = [
        {
            "title": result.metadata.get("title"),
            "page_url": result.metadata.get("page_url"),
            "summary": result.get_text(),
            "score": result.get_score()
        }
        for result in results
    ]
    return response


def display_cards(talks):
    # Create a grid of cards to display the talks
    cols = st.columns(3)
    for col, talk in zip(cols, talks):
        with col:
            st.subheader(f"[{talk.get('title')}]({talk.get('page_url')})")
            st.write(talk.get("summary"))
            st.write(talk.get("score"))
            # st.link_button("Watch the talk", talk.get("page_url"))


def main():
    st.title("TED Talk Finder")

    user_query = st.text_input("Enter your query to find the best TED talks:", "")

    if user_query:
        result_talks = retrieve_similar_talks(user_query)
        display_cards(result_talks)

if __name__ == "__main__":
    main()
