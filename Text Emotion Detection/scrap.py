import requests
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd

def scrape_amazon_reviews(url):
    # Fetch the HTML content of the Amazon product page
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to fetch the page")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all review elements
    review_elements = soup.find_all('div', class_='a-section review')

    # Extract review information
    reviews = []
    for review in review_elements:
        reviewer_name = review.find('span', class_='a-profile-name').get_text(strip=True)
        rating = review.find('i', class_='review-rating').get_text(strip=True)
        review_date = review.find('span', class_='review-date').get_text(strip=True)
        review_text = review.find('span', class_='review-text').get_text(strip=True)

        review_info = {
            'Reviewer Name': reviewer_name,
            'Rating': rating,
            'Review Date': review_date,
            'Review Text': review_text
        }
        reviews.append(review_info)

    return reviews

# Streamlit UI
st.title("Amazon Review Scraper")

# Input box for pasting the Amazon product URL
amazon_url = st.text_input("Paste Amazon Product URL")

if amazon_url:
    # Button to trigger scraping
    if st.button("Scrape Reviews"):
        reviews = scrape_amazon_reviews(amazon_url)

        # Display scraped reviews
        if reviews:
            st.write("Scraped Reviews:")
            df = pd.DataFrame(reviews)
            st.write(df)

            # Export to PDF or Excel
            export_format = st.selectbox("Select export format", ["None", "PDF", "Excel"])
            if export_format != "None":
                if export_format == "PDF":
                    st.write("Exporting to PDF...")
                    df.to_pdf("reviews.pdf")
                    st.success("Reviews exported to PDF!")
                elif export_format == "Excel":
                    st.write("Exporting to Excel...")
                    df.to_excel("reviews.xlsx", index=False)
                    st.success("Reviews exported to Excel!")
        else:
            st.warning("No reviews found on the provided URL")

# Display the app in the browser
if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.sidebar.title("Scrap The Reviews")
    app_mode = st.sidebar.radio("Go to", ["Home", "About"])
    if app_mode == "Home":
        st.write("This is the Home page.")
    elif app_mode == "About":
        st.write("This is the About page.")
