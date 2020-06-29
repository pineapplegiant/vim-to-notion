import os
import sys
from uuid import uuid1
from datetime import datetime, date
import argparse
from dotenv import load_dotenv
from pprint import pprint
import frontmatter
from notion.client import NotionClient
from notion.collection import NotionDate
from md2notion.upload import upload
from notion.block import TodoBlock
from notion.block import PageBlock

# Before running please put your environment variables in your .env file.
# Python will automatically store these files if they're in the same dir.

def login_to_notion():
    """Will source the .env file and return credentials"""

    load_dotenv() # Grab dotenv tokens from .env file

    # MY .ENV TOKENS
    token_v2 = os.environ.get("API_TOKEN") # My API Token
    collection_view = os.environ.get("COLLECTION_VIEW") # My URL to the table page

    # Login to Notion
    client = NotionClient(token_v2=token_v2)

    # Grab Table of Blog Posts
    cv = client.get_collection_view(collection_view, force_refresh=True)

    return cv, token_v2, collection_view, client


def get_articles(cv):
    """Given an instance of the CollectionsView, it will loop through the table
    page view creating and returning a list of articles"""
    blog_posts = {} # {'title': 'page_id',]
    for row in cv.collection.get_rows():
        blog_posts[f"{row.title}"] = row.id

    return blog_posts

def get_args():
    """Grab arguments from stdin"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="pass in a file to upload to notion")
    args = parser.parse_args()

    return args

def main():
    args = get_args()

    # Load the file passed in through args
    post = frontmatter.load(args.file)
    title = post['title']
    tags = post['tags']
    date = post['date']
    last_edited = post['last_edited']

    # Get everything for notion: CV is the CollectionViewPageBlock "Table Page"
    cv, token_v2, collection_view, client = login_to_notion()
    collection = cv.collection
    dict_of_articles = get_articles(cv)
    print(f"There are {len(dict_of_articles)} articles: \n")
    pprint(dict_of_articles)

    if title in dict_of_articles:
        # Delete then Upload Blog Post
        print(f"\n\n'{title}'\nALREADY IN LIST OF ARTICLES ON NOTION...")
        print(f"\tUPDATING ARTICLE!")

        # Grab the URL_ID from the dict_of_articles
        url_to_blog_page = dict_of_articles[title]

        # Select the page in notion
        blog_page = client.get_block(url_to_blog_page)

        # If it was edited on Notion Don't fuck with the Article:
        if blog_page.edited_on_notion:
            print("\n\n\tBRO WTFF!!!!!!!!!!")
            print("You edited this on Notion, I'm not fucking with this article")
            print("Here's the URL so you can sync the changes:")
            print(f"{collection_view}&p={blog_page.id}")

            print("\nExiting...\n")
            return

        # Delete Blog Page
        blog_page.remove()

    else:
        # Upload Blog since it's not in the list
        print(f"\n\n'{title}'\nNOT IN NOTION LIST")
        print(f"\tUPLOADING NEW ARTICLE INTO NOTION\n")

    # Upload New Blog Page
    row = cv.collection.add_row()

    # Add Metadata
    try:
        row.title = title
        if tags:
            row.tags = tags
        if date:
            row.date = NotionDate(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
        if last_edited:
            row.last_edited = NotionDate(datetime.strptime(last_edited, "%Y-%m-%d %H:%M:%S"))
    except KeyError as e:
        print("\n\tERROR")
        print(e)
        print("Make sure you're formatting your FrontMatter Correctly:")
        print('tags: ["psychology", "productivity", "book review", "self help"]')
        print("title: 'My Title\n'")
        print("date: '2020-06-20 16:21:41'")

    # Re-Generate new List of articles to find the new ID
    dict_of_articles = get_articles(cv)

    url_to_blog_page = dict_of_articles[title]

    # Grab the whole row as a page
    blog_page = client.get_block(url_to_blog_page)

    # Add a text block and dump all the content in
    with open(args.file, "r", encoding="utf-8") as mdFile:
        # Set Blog Page to the actual content of the page
        blog_page = blog_page.children.add_new(TodoBlock)
        upload(mdFile, blog_page)

    # Delete the YAML frontmatter of the md file
    del(blog_page.children[1])

# Execute main file
if __name__=="__main__":
    main()
