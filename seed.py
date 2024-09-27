import json

from models import Author, Quote


def save_data():
    with open("authors.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
        for el in data:
            try:
                authors = Author.objects(fullname=el.get("fullname"))
                if not authors:
                    author = Author(fullname=el.get("fullname"), born_date=el.get("born_date"),
                                    born_location=el.get("born_location"), description=el.get("description"))
                    author.save()
            except Exception as e:
                print(e)
                
    with open("quotes.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
        for el in data:
            try:
                author, *_ = Author.objects(fullname=el.get("author"))
                quote = Quote(tags=el.get("tags"), author=author,
                                quote=el.get("quote"))
                quote.save()
            except Exception as e:
                print(e)
                
            
            
if __name__=="__main__":
    save_data()