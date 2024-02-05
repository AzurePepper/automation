import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import argparse

def scrape_contents_for_date(date_object):
    """
    Web scraping function to retrieve specific information for a given date.

    Parameters:
    - date_object (datetime): The date for which information needs to be scraped.

    For future use, the URL and the tag to find should be decided and changed. (Search #KEY_VAR)
    """

    # Format the date as 'YYYY-MM-DD'
    date = date_object.strftime("%Y-%m-%d")
    day_name = date_object.strftime("%a")

    # Construct the URL with the provided date
    url = f"https://homepage.com/daily-content?date={date}"

    # Make a request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class 'content'
        content = soup.find('div', class_='content')

        # Extract the contents from the 'workout' div
        if content:
            # Find titles and descriptions
            titles = content.find_all(class_="DailyTitle")
            descs = content.find_all(class_="DailyContent")

            # Print the contents for the provided date
            print(f"<<Content for {date} {day_name}>>")
            for title, desc in zip(titles, descs):
                print(title.text)
                desc_text = desc.get_text(separator="\n")
                print(desc_text)
                print()
            print("-" * 20)
        else:
            print(f"No content information found for {date}")
    else:
        print(f"Request failed for date {date} with status code: {response.status_code}")


def main():
    """
    Main function to retrieve information for a specified number of days.
    Retrieves the number of days from the command-line arguments.
    """

    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Scrape information for a specified number of days.')
    parser.add_argument('num_days', type=int, help='Number of days to retrieve information')

    # Parse command-line arguments
    args = parser.parse_args()

    # Start date (today)
    start_date = datetime.now()
    while start_date.weekday() > 5:
        start_date += timedelta(days=1)

    # Number of days to iterate
    num_days = args.num_days

    for day in range(num_days):
        # Calculate the date for the current iteration
        current_date_object = start_date + timedelta(days=day)

        # Call the scraping function for the current date
        scrape_contents_for_date(current_date_object)

if __name__ == "__main__":
    main()

