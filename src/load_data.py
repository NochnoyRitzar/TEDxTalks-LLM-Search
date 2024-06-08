import pandas as pd
from llama_index.core import Document


def convert_df_to_documents(df_path: str) -> list[Document]:
    """
    Convert a pandas dataframe to a list of llama-index Document objects.
    :param df_path: path to local pandas dataframe
    :return:
    """
    df = pd.read_json(df_path)

    documents = [
        Document(
            # @TODO: Consider using other columns
            text=row["summary"],
            metadata={
                "page_url": row["page_url"],
                "title": row["title"],
                "duration": int(row["duration"]),
                "topics_list": row["topics_names"].split(", "),
            }
        )
        for _, row in df.iterrows()
    ]

    return documents
