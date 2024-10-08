import requests
from bs4 import BeautifulSoup
import random

class RecipeAPI:
    def get_latest_recipes(self):
        url = "https://www.bonappetit.com/feed/rss"
        response = requests.get(url)

        if response.status_code == 200:
            # Use the lxml XML parser
            soup = BeautifulSoup(response.content, 'lxml-xml')
            items = soup.find_all('item')

            # Extract title and content of each article
            recipes = []
            for item in items:
                title = item.title.text
                link = item.link.text
                
                # Debugging: Print title and link
                print(f"Title: {title}, Link: {link}")

                # Check if link is valid before making a request
                if link:
                    # Fetch the article content
                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.content, 'html.parser')
                        paragraphs = article_soup.find_all('p')
                        full_content = "\n".join([p.text for p in paragraphs])
                        recipes.append((title, full_content))
                    else:
                        print(f"Failed to retrieve article: {article_response.status_code}")
                else:
                    print(f"Invalid link for title: {title}")

            return recipes  # Return a list of recipes (title, full content)
        else:
            print(f"Failed to retrieve recipes: {response.status_code}")
            return []

    def get_random_recipe(self):
        recipes = self.get_latest_recipes()
        if recipes:
            return random.choice(recipes)  # Return a random recipe
        else:
            return None, None

# Example usage
if __name__ == "__main__":
    api = RecipeAPI()
    title, full_content = api.get_random_recipe()
    if title and full_content:
        print(f"Title: {title}\n\n{full_content}")
    else:
        print("No recipes found.")
