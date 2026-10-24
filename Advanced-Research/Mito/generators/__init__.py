"""
Mito Generators
Lorem ipsum, passwords, test data, mock data, fixtures
"""

import random
import string
import secrets
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


def lorem_paragraphs(count: int = 3) -> str:
    paragraphs = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa.",
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis.",
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
        "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias.",
    ]
    return "\n\n".join(paragraphs[:count])


def lorem_words(count: int = 50) -> str:
    words = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit".split()
    return " ".join(random.choices(words, k=count))


def password(length: int = 16, uppercase: int = 2, digits: int = 2, symbols: int = 2) -> str:
    chars = list(string.ascii_lowercase)
    pwd = [secrets.choice(string.ascii_uppercase) for _ in range(uppercase)]
    pwd += [secrets.choice(string.digits) for _ in range(digits)]
    pwd += [secrets.choice("!@#$%^&*") for _ in range(symbols)]
    pwd += [secrets.choice(chars) for _ in range(length - len(pwd))]
    random.shuffle(pwd)
    return "".join(pwd)


def uuid4() -> str:
    return str(uuid.uuid4())


def uuid7() -> str:
    import time
    ts = int(time.time() * 1000)
    rand = secrets.randbits(74)
    uuid_int = (ts << 74) | rand
    uuid_int &= ~(0xF << 76)
    uuid_int |= 7 << 76
    uuid_int &= ~(3 << 62)
    uuid_int |= 2 << 62
    return str(uuid.UUID(int=uuid_int))


def nanoid(length: int = 21, alphabet: str = None) -> str:
    alphabet = alphabet or "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def mock_user() -> Dict[str, Any]:
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
    first = random.choice(first_names)
    last = random.choice(last_names)
    return {
        "id": uuid4(),
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower()}@example.com",
        "username": f"{first.lower()}{last.lower()}{random.randint(1, 99)}",
        "phone": f"+1{random.randint(2000000000, 9999999999)}",
        "avatar": f"https://i.pravatar.cc/150?u={uuid4()}",
        "created_at": random_date().isoformat(),
    }


def mock_company() -> Dict[str, Any]:
    prefixes = ["Acme", "Globex", "Initech", "Umbrella", "Stark", "Wayne", "Cyberdyne"]
    suffixes = ["Corp", "Inc", "Ltd", "LLC", "Systems", "Technologies", "Solutions"]
    name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
    return {
        "id": uuid4(),
        "name": name,
        "domain": f"{name.lower().replace(' ', '')}.com",
        "industry": random.choice(["Tech", "Finance", "Healthcare", "Retail", "Manufacturing"]),
        "employees": random.randint(10, 10000),
        "founded": random.randint(1990, 2023),
    }


def mock_product() -> Dict[str, Any]:
    adjectives = ["Premium", "Ultra", "Pro", "Advanced", "Elite", "Classic"]
    nouns = ["Widget", "Gadget", "Doohickey", "Thingamajig", "Whatchamacallit"]
    return {
        "id": uuid4(),
        "name": f"{random.choice(adjectives)} {random.choice(nouns)}",
        "price": round(random.uniform(9.99, 999.99), 2),
        "sku": f"SKU-{random.randint(10000, 99999)}",
        "in_stock": random.choice([True, True, True, False]),
        "rating": round(random.uniform(1, 5), 1),
    }


def mock_post() -> Dict[str, Any]:
    titles = [
        "Getting Started with AI", "10 Tips for Better Code",
        "Understanding Distributed Systems", "The Future of Web Development",
        "Building Scalable Applications", "Modern DevOps Practices",
    ]
    return {
        "id": uuid4(),
        "title": random.choice(titles),
        "body": lorem_paragraphs(2),
        "author": mock_user()["first_name"],
        "tags": random.sample(["python", "ai", "devops", "cloud", "web", "api"], 3),
        "published_at": random_date().isoformat(),
        "views": random.randint(100, 50000),
    }


def mock_list(generator, count: int = 5) -> List[Dict]:
    return [generator() for _ in range(count)]


def random_date(start: datetime = None, end: datetime = None) -> datetime:
    start = start or datetime(2020, 1, 1)
    end = end or datetime.now()
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def random_ip() -> str:
    return f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def random_mac() -> str:
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))


def random_color() -> str:
    return f"#{random.randint(0, 0xFFFFFF):06x}"


def seed(seed_value: int):
    random.seed(seed_value)
