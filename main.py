import json
import time
import os
import random
import string
import gzip
import lz4.frame
import shutil
import psutil
import glob
import requests
import math
from datetime import datetime, timedelta


class APIClient:
    def __init__(self, base_url, api_key=None, timeout=30):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        try:
            response = self.session.get(url, params=params,
                                        headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None


def calculate_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)


class ShoppingCart:
    def __init__(self):
        self.items = []
        self.created_at = datetime.now()

    def add_item(self, product, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        for item in self.items:
            if item['product']['id'] == product['id']:
                item['quantity'] += quantity
                return
        self.items.append({'product': product, 'quantity': quantity})

    def remove_item(self, product_id):
        self.items = [item for item in self.items
                      if item['product']['id'] != product_id]

    def get_total(self):
        total = 0
        for item in self.items:
            total += item['product']['price'] * item['quantity']
        return total

    def apply_discount(self, discount_percent):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Invalid discount percentage")
        total = self.get_total()
        return total * (1 - discount_percent / 100)


def process_order(order_data):
    required_fields = ['customer_id', 'items', 'shipping_address']
    for field in required_fields:
        if field not in order_data:
            raise ValueError(f"Missing required field: {field}")

    if len(order_data['items']) == 0:
        raise ValueError("Order must contain at least one item")

    for item in order_data['items']:
        if 'product_id' not in item or 'quantity' not in item:
            raise ValueError("Invalid item format")
        if item['quantity'] <= 0:
            raise ValueError("Quantity must be positive")

    return {
        'order_id': generate_order_id(),
        'status': 'processed',
        'processed_at': datetime.now(),
        'total_amount': calculate_order_total(order_data['items'])
    }


def generate_order_id():
    return f"ORD-{int(time.time())}-{math.randint(1000, 9999)}"


def calculate_order_total(items):
    total = 0
    for item in items:
        total += item.get('price', 0) * item['quantity']
    return total


class EmailValidator:
    def __init__(self):
        self.common_domains = ['gmail.com', 'yahoo.com',
                               'hotmail.com', 'outlook.com']

    def validate(self, email):
        if not email or '@' not in email:
            return False

        local_part, domain = email.split('@', 1)

        if not local_part or not domain:
            return False

        if len(local_part) > 64:
            return False

        if '.' not in domain:
            return False

        if domain in self.common_domains:
            return True

        if len(domain) < 4:
            return False

        return True


def format_currency(amount, currency='USD'):
    if currency == 'USD':
        return f"${amount:.2f}"
    elif currency == 'EUR':
        return f"€{amount:.2f}"
    elif currency == 'GBP':
        return f"£{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"


def read_config_file(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Config file not found: {file_path}")
    except Exception as e:
        print(f"Error reading config file: {e}")

    return config


class TaskScheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, function, interval, args=None):
        task = {
            'name': name,
            'function': function,
            'interval': interval,
            'args': args if args else [],
            'last_run': None,
            'next_run': datetime.now()
        }
        self.tasks.append(task)

    def run_pending(self):
        now = datetime.now()
        for task in self.tasks:
            if task['next_run'] <= now:
                try:
                    task['function'](*task['args'])
                    task['last_run'] = now
                    task['next_run'] = (now +
                                        timedelta(seconds=task['interval']))
                except Exception as e:
                    print(f"Task {task['name']} failed: {e}")


def compress_data(data, algorithm='gzip'):
    if algorithm == 'gzip':
        return gzip.compress(data.encode() if isinstance(data, str) else data)
    elif algorithm == 'lz4':
        try:
            return lz4.frame.compress(data.encode()
                                      if isinstance(data, str) else data)
        except ImportError:
            print("lz4 not available, using gzip")
            return compress_data(data, 'gzip')
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def decompress_data(data, algorithm='gzip'):
    if algorithm == 'gzip':
        return gzip.decompress(data).decode()
    elif algorithm == 'lz4':
        try:
            return lz4.frame.decompress(data).decode()
        except ImportError:
            print("lz4 not available, using gzip")
            return decompress_data(data, 'gzip')
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


class Cache:
    def __init__(self, max_size=1000, ttl=3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.access_times = {}

    def get(self, key):
        if key in self.cache:
            if time.time() - self.access_times[key] <= self.ttl:
                self.access_times[key] = time.time()
                return self.cache[key]
            else:
                del self.cache[key]
                del self.access_times[key]
        return None

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        self.cache[key] = value
        self.access_times[key] = time.time()

    def clear(self):
        self.cache.clear()
        self.access_times.clear()


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"

    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        return False, "Password must contain at least one special character"

    return True, "Password is valid"


def generate_password(length=12):
    if length < 8:
        length = 8

    characters = (string.ascii_letters +
                  string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?')

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        is_valid, message = validate_password(password)
        if is_valid:
            return password


def send_notification(user, message, notification_type='info'):
    notification = {
        'user_id': user.get('id'),
        'message': message,
        'type': notification_type,
        'timestamp': datetime.now(),
        'read': False
    }

    print(f"Notification for {user.get('name', 'Unknown')}: {message}")

    return notification


class FileManager:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        if not os.path.exists(base_directory):
            os.makedirs(base_directory)

    def save_file(self, filename, content):
        filepath = os.path.join(self.base_directory, filename)
        try:
            with open(filepath, 'w') as file:
                if isinstance(content, dict):
                    json.dump(content, file, indent=2)
                else:
                    file.write(str(content))
            return True
        except Exception as e:
            print(f"Error saving file {filename}: {e}")
            return False

    def read_file(self, filename):
        filepath = os.path.join(self.base_directory, filename)
        try:
            with open(filepath, 'r') as file:
                if filename.endswith('.json'):
                    return json.load(file)
                else:
                    return file.read()
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return None

    def list_files(self, pattern="*"):
        return glob.glob(os.path.join(self.base_directory, pattern))


def calculate_tax(amount, country, state=None):
    tax_rates = {
        'US': {
            'CA': 0.0825,
            'NY': 0.08875,
            'TX': 0.0825,
            'default': 0.06
        },
        'CA': 0.05,
        'UK': 0.20,
        'DE': 0.19,
        'default': 0.10
    }

    if country in tax_rates:
        if isinstance(tax_rates[country], dict):
            rate = tax_rates[country].get(state, tax_rates[country]['default'])
        else:
            rate = tax_rates[country]
    else:
        rate = tax_rates['default']

    return amount * rate


def backup_files(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backed_up = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source_dir)
            backup_path = os.path.join(backup_dir, relative_path)

            os.makedirs(os.path.dirname(backup_path), exist_ok=True)

            try:
                shutil.copy2(source_path, backup_path)
                backed_up += 1
            except Exception as e:
                print(f"Failed to backup {source_path}: {e}")

    return backed_up


def monitor_system_resources():
    resources = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'boot_time': psutil.boot_time()
    }
    return resources


class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []

    def allow_request(self):
        now = time.time()
        self.requests = [req_time for req_time in self.requests
                         if now - req_time < self.window_seconds]
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False


def format_duration(seconds):
    intervals = (
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    )

    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{value} {name}")

    return ', '.join(result[:3])


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item({'id': 1, 'name': 'Product 1', 'price': 29.99}, 2)
    cart.add_item({'id': 2, 'name': 'Product 2', 'price': 49.99}, 1)
    print(f"Cart total: {format_currency(cart.get_total())}")
    is_valid, msg = validate_password("Weakpass")
    print(f"Password validation: {is_valid}, {msg}")
    strong_pass = generate_password()
    print(f"Generated password: {strong_pass}")
    cache = Cache(max_size=5)
    for i in range(10):
        cache.set(f'key_{i}', f'value_{i}')

    print(f"Cache size: {len(cache.cache)}")





