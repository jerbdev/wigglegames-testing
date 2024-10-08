import axios from 'axios';  // Use axios for HTTP requests
import { parseStringPromise } from 'xml2js';  // To parse the RSS feed

// Still in development for web.

export const getRandomRecipe = async () => {
  const url = "https://www.bonappetit.com/feed/rss";
  try {
    const response = await axios.get(url);

    // Parse the RSS feed XML to JavaScript object
    const parsedData = await parseStringPromise(response.data);
    const items = parsedData.rss.channel[0].item;

    // Extract title, link, and description
    const recipes = items.map(item => ({
      title: item.title[0],
      link: item.link[0],
      description: item.description ? item.description[0] : "No description available."
    }));

    // Select a random recipe
    const randomRecipe = recipes[Math.floor(Math.random() * recipes.length)];
    return {
      title: randomRecipe.title,
      fullContent: randomRecipe.description,
      link: randomRecipe.link
    };
  } catch (error) {
    console.error("Error fetching the recipes:", error);
    return null;
  }
};
