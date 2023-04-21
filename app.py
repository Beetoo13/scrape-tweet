import snscrape.modules.twitter as sntwitter
import json, requests

tweet_ids = []
not_downloaded = []


def scrape_tweet():
    for tweet_id in tweet_ids:
        try:
            response = sntwitter.TwitterTweetScraper(tweet_id).get_items()

            for res in response:
                try:
                    tweet = json.loads(res.json())
                    media = tweet["media"]
                    print(f"Tweet '{tweet_id}':")
                    for image in media:
                        image_name = parse_image_name(image['fullUrl'])
                        img_data = requests.get(image['fullUrl']).content
                        with open(f'{image_name}.jpg', 'wb') as handler:
                            handler.write(img_data)
                        print(f"\t- {image['fullUrl']}")
                except Exception as e:
                    print(f"Error downloading {res.id}: {e}")
        except Exception as e:
            print(
                f"There was an error getting the tweet ({tweet_id}) information: {e}"
            )
            not_downloaded.append(tweet_id)

    print(f"not_downloaded list: {not_downloaded}")


def main():
    get_links()
    scrape_tweet()


def get_links():
    urls_file = open("links.txt", "r")
    url_lines = urls_file.readlines()
    for url in url_lines:
        twt_id = url.split("/")
        parsed_twt_id = twt_id[5].split("?")
        tweet_ids.append(parsed_twt_id[0])


def parse_image_name(image_url):
    name_path = image_url.split("/")
    name = name_path[4].split("?")
    return name[0]


if __name__ == "__main__":
    main()