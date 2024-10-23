import os
import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import random
import groq
import sys

load_dotenv()
class NewsGenerator():
    def __init__(self, model_name):
        self.model = ChatGroq(model_name=model_name)
        self.system_message_content = """
        Use the model to generate a set of fictitious news articles on different topics: politics, economy, sports, science, etc.
        Requirements:

            Model: use the model to generate the news.

            Quantity: Generate approximately between 500 and 1000 unique and fictitious news articles.

            Length per article: Each news article should be between 300 and 500 words.

            Structure:
                Title: Each article should have an attractive and relevant title.
                Author: Assign a fictitious author for each news article.
                Date: Include a fictitious date for each article.
                Body: The body of the text should read like a coherent and informative news article, as if it came from a reliable news source.

            Diversity of topics: Ensure to cover a wide range of topics, including but not limited to:
                Politics: Elections, political scandals, policy changes, etc.
                Economy: Market trends, economic policies, trade agreements, etc.
                Sports: International competitions, match results, player transfers, etc.
                Science: Technological advances, medical discoveries, environmental studies, etc.
                Culture/Entertainment: Celebrity news, film reviews, fashion, cultural festivals, etc.
                Global events: Disasters, international relations, emerging nations, etc.
                Technology: Innovations in AI, space exploration, cybersecurity threats, etc.

            Tone and coherence: Ensure that each article uses a tone that matches the topic (e.g., formal for politics, enthusiastic for sports) and that the language is coherent and believable. Avoid extreme repetitions of phrases or ideas between articles to maintain originality and creativity.

            Verisimilitude: Each article should seem credible enough to be mistaken for real-world news. The fictitious events should include enough details (locations, quotes, statistics) to feel grounded in reality.

            Creativity: You are free to invent names, locations, events, companies, and fictitious figures, but ensure they are varied and realistic within the context of the news.

            Output format: Ensure that each news article is clearly separated, with the title, author, and date correctly formatted above the body of the text. 

        Example of output format:
        Title: New Environmental Policy Shakes Global Markets
        Author: Jane Doe
        Date: June 12, 2024
        Topic: {topic}

        In a surprising move today, the Global Environmental Council announced a set of new regulations aimed at reducing carbon emissions. Experts predict that these measures could drastically alter the stock market, especially in the energy and transportation sectors...
        """

    def generate_new(self):

        topics=[
            "Politics", "Economy", "Sports", "Science",
            "Culture/Entertainment", "Global events", "Technology"
        ]

 
        topic = random.choice(topics)
        news_prompt = f"""Generate a fictitious news article on the topic of {topic}."""

        self.system_message_content = self.system_message_content.format(
            topic=topic
        )

        messages = [
            SystemMessage(content=self.system_message_content),
            HumanMessage(content=news_prompt)
        ]

        print(f"generate a news article on the topic of {topic}")
        try:
            return self.model.invoke(messages).content.replace(
                        "Here is a synthetic note:", ""
                    )
        except groq.APIConnectionError as e:
                    print("The server could not be reached")
                    print(e.__cause__)

    def generate_news(self, num_news:int, wait_time:int):
        for i in range(num_news):
            if i != 0:
                time.sleep(wait_time)

            yield self.generate_new()


def main():
    news_generator = NewsGenerator("llama3-70b-8192")
    
    num_news = 100
    wait_time = 1
    with open("synthetic_dataset_generation/synthetic_news.txt", "a",encoding="utf-8") as f:
        for i, new in enumerate(
                news_generator.generate_news(num_news, wait_time)
            ):
            sys.stdout.write(f"\rGenerated new {i + 1}/{num_news}\n")
            sys.stdout.flush()
            f.write(new)
            f.write("\n")
            f.write("-" * 100)
            f.write("\n")
        print("\n")

if __name__ == "__main__":
    main()  
