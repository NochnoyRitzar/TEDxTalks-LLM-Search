import os
import pickle
from openai import OpenAI
from utilities import load_csv_data
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI()


def get_openai_embedding(text):
   text = text.replace("\n", " ")
   return openai_client.embeddings.create(input=[text], model="text-embedding-ada-002").data[0].embedding


def main():
   df = load_csv_data(os.path.join('data', 'preprocessed', 'preprocessed_ted_talks.csv'))
   df['combined'] = df['title'] + ' ' + df['summary']

   embeddings = df['combined'].apply(lambda text: get_openai_embedding(text))

   os.makedirs(os.path.join('data', 'embeddings'), exist_ok=True)
   with open(os.path.join('data', 'embeddings', 'openai_embeddings.pkl'), 'wb') as f:
        pickle.dump(embeddings, f)

if __name__ == "__main__":
   main()