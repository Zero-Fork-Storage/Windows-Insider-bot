
from app import WIB


client = WIB()

if __name__ == "__main__":
    client.load_extensions(["cogs.rss", "cogs.system"])
    client.run()
