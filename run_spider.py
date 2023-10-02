# run_spider.py
import argparse
import json
import redis

# Define a mapping of keywords to JSON files
keyword_to_params = {
    "vr": ("data/viva_real.json", "viva_real:start_urls"),
    "zap": ("data/zap.json", "zap:start_urls"),
    "qa": ("data/quinto_andar.json", "quinto_andar:start_urls")
}


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Read JSON data from a file and save it to a Redis key.")
    parser.add_argument("keyword", choices=keyword_to_params.keys(), help="Keyword to select JSON file")
    args = parser.parse_args()

    # Create a Redis connection
    redis_client = redis.StrictRedis(host='192.168.1.245', port=6379, db=0)

    try:
        # Get the corresponding JSON file for the keyword
        params = keyword_to_params[args.keyword]
        json_file_name = params[0]
        redis_key = params[1]

        # Read JSON data from the specified file
        with open(json_file_name, 'r', encoding='utf-8') as json_file:
            request_data = json.load(json_file)

        # Convert the JSON data to a string
        request_json = json.dumps(request_data)

        # Set the JSON string to the Redis key
        redis_client.rpush(redis_key, request_json)

        print(f"Request data saved to '{redis_key}' in Redis.")
    except KeyError:
        print(f"Error: The specified keyword '{args.keyword}' is not recognized.")
    except FileNotFoundError:
        print(f"Error: The specified JSON file '{json_file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
