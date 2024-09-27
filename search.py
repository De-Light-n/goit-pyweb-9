from pprint import pprint
import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_tags(tags: tuple[str]) -> list[str]:
    result = []
    for tag in tags:
        quotes = Quote.objects(tags__iregex=tag)
        for quote in quotes:
            if quote.quote in result:
                continue
            result.append(quote.quote)
    return result

@cache
def find_by_author(name: str)->list[str]:
    authors = Author.objects(fullname__iregex=name)
    result = {}
    for a in authors:
        quote = Quote.objects(author=a)
        result.update({a.fullname:[q.quote for q in quote]})
    return result


def main():
    while True:
        user_input = input("Search: ")
        if user_input == "exit":
            print("Goodbye")
            break 
        try:
            command, value = user_input.split(":")
            command = command.lower().strip()
            value = [v.lower().strip() for v in value.split(",")]
        except Exception as e:
            print("Invalid command")
            continue
        if command == "tags" or command == "tag":
            pprint(find_by_tags(tuple(value)))
        elif command == "name":
            pprint(find_by_author(*value))
        else:
            print("Invalid command")


if __name__=="__main__":
    main()        
