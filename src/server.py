from flask import *
import feedparser 
import requests

app = Flask(__name__)

class RSS():

    def get_entries(rss_link):
        """
            RSS is pulled from the web, parsed and returns entries.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
        } # Set user agent header
        try:
            response = requests.get(rss_link,headers=headers) #Pull RSS feed
        except: 
            return False # If it gives an error, it returns False.

        if response.ok: # If the request was made successfully
            parsed_feed = feedparser.parse(response.text) # Parses the feed
            if parsed_feed.bozo: # Returns False if the feed is incorrect and could not be parsed
                return False
            return parsed_feed.entries # If successful, return entries in the feed
        return False
    

    def get_attributes(entry):
        """
            Returns the attributes in the entry as a dictionary
        """
        return {
            "author":entry.get("author",""),
            "title":entry.get("title",""),
            "summary":entry.get("summary",""),
            "published":entry.get("published",""),
            "tags":entry.get("tags",[]),
            "link":entry.get("link","")
        }


@app.route("/",methods=['GET', 'POST'])
def index():
    """
        Index of the page
    """
    if request.method == 'POST': #  If a request is made with the POST method
        rss_link = request.form.get("rss_link","") # Get RSS link
        theme = request.form.get("theme","") # Get theme 
        entries = RSS.get_entries(rss_link) # Get entries
        
        if entries:
            entry_list = []
            for entry in entries:
                entry_list.append(RSS.get_attributes(entry)) # Get all RSS entries and save them to a list
            return render_template(f"{theme}.html",entries=entry_list) # Return with the selected theme


        else:
            return render_template("error.html") # Return error template if RSS.get_entries value is False


    elif request.method == 'GET': # If a request is made with the GET method
        return render_template("search.html") # Return the search template

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8000) # Run the app on https://127.0.0.1:8000/
