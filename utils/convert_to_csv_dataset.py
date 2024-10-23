import re
import csv

def read_news_articles(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    articles = content.split('-' * 100)
    articles = [article.strip() for article in articles if article.strip()]
    
    return articles 


def parse_article(article_text):
    title_match = re.search(r'\*\*Title:\*\* (.+)', article_text)
    author_match = re.search(r'\*\*Author:\*\* (.+)', article_text)
    date_match = re.search(r'\*\*Date:\*\* (.+)', article_text)
    body_match = re.search(r'\*\*Date:\*\* .+\n\n(.+)', article_text, re.DOTALL)

    title = title_match.group(1).strip() if title_match else ''
    author = author_match.group(1).strip() if author_match else ''
    date = date_match.group(1).strip() if date_match else ''
    body = body_match.group(1).strip() if body_match else ''

    body = re.sub(r'Here is a fictitious news article on the topic of .+:\n', '', body)
    body = body.strip()

    return {
        'title': title,
        'author': author,
        'date': date,
        'content': body
    }


def convert_to_csv(articles, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['idx','title', 'author', 'date', 'content'])
        writer.writeheader()
        for i,article in enumerate(articles):
            writer.writerow({
                'idx': i,
                'title': article['title'],
                'author': article['author'],
                'date': article['date'],
                'content': article['content']
            })



def main():
    articles = read_news_articles('synthetic_dataset_generation/synthetic_news.txt')
    articles = [parse_article(article) for article in articles]
    convert_to_csv(articles, 'synthetic_dataset_generation/synthetic_news.csv')

if __name__ == "__main__":
    main()