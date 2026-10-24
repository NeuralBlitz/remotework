-----
name: patterns
description: >
  Expert in software design patterns and architectural solutions. Use this skill 
  for solving recurring software design problems, selecting appropriate patterns 
  for specific contexts, refactoring code to use patterns, and explaining pattern 
  trade-offs. Covers creational, structural, behavioral, architectural, and 
  concurrency patterns with practical examples.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: software-development
  tags: [design-patterns, architecture, refactoring, software-design]

# Software Design Patterns

Covers: **Creational Patterns · Structural Patterns · Behavioral Patterns · Architectural Patterns · Concurrency Patterns · Anti-Patterns**

-----

## Pattern Overview

### Pattern Classification

| Category | Purpose | Common Patterns |
|----------|---------|-----------------|
| **Creational** | Object creation mechanisms | Factory, Builder, Singleton, Prototype |
| **Structural** | Object composition | Adapter, Bridge, Composite, Decorator, Facade, Proxy |
| **Behavioral** | Object communication | Observer, Strategy, Command, State, Chain of Responsibility |
| **Architectural** | System-level structure | MVC, MVVM, Repository, Unit of Work, CQRS |
| **Concurrency** | Multi-threaded patterns | Thread Pool, Producer-Consumer, Read-Write Lock |

### When to Use Patterns

```
Consider a pattern when:
├── You recognize the problem as a recurring pattern
├── You understand the consequences (complexity trade-off)
├── You can explain why you chose it
├── The team understands the pattern
└── It doesn't over-engineer simple solutions

Avoid patterns when:
├── You don't have the problem the pattern solves
├── Simpler solutions work fine
├── Team doesn't understand the pattern
├── It's used just for "coolness"
```

-----

## Creational Patterns

### Factory Method

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class Notification(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> Dict[str, Any]:
        pass

class EmailNotification(Notification):
    def send(self, message: str, recipient: str) -> Dict[str, Any]:
        # Email sending logic
        return {
            'status': 'sent',
            'channel': 'email',
            'recipient': recipient,
            'message': message
        }

class SMSNotification(Notification):
    def send(self, message: str, recipient: str) -> Dict[str, Any]:
        # SMS sending logic
        return {
            'status': 'sent',
            'channel': 'sms',
            'recipient': recipient,
            'message': message
        }

class PushNotification(Notification):
    def send(self, message: str, recipient: str) -> Dict[str, Any]:
        # Push notification logic
        return {
            'status': 'sent',
            'channel': 'push',
            'recipient': recipient,
            'message': message
        }

class NotificationFactory:
    """Factory for creating notification instances"""
    
    _creators = {
        'email': EmailNotification,
        'sms': SMSNotification,
        'push': PushNotification
    }
    
    @classmethod
    def create(cls, notification_type: str) -> Notification:
        creator = cls._creators.get(notification_type.lower())
        if not creator:
            raise ValueError(f"Unknown notification type: {notification_type}")
        return creator()
    
    @classmethod
    def register(cls, notification_type: str, creator_class):
        """Allow dynamic registration of new notification types"""
        cls._creators[notification_type.lower()] = creator_class

# Usage
factory = NotificationFactory()
email_notif = factory.create('email')
sms_notif = factory.create('sms')
```

### Abstract Factory

```python
# Families of related objects
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class TextField(ABC):
    @abstractmethod
    def render(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass

# Windows family
class WindowsButton(Button):
    def render(self):
        return "<WindowsButton>"

class WindowsTextField(TextField):
    def render(self):
        return "<WindowsTextField>"

class WindowsCheckbox(Checkbox):
    def render(self):
        return "<WindowsCheckbox>"

# Mac family
class MacButton(Button):
    def render(self):
        return "[MacButton]"

class MacTextField(TextField):
    def render(self):
        return "[MacTextField]"

class MacCheckbox(Checkbox):
    def render(self):
        return "[MacCheckbox]"

# Abstract factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_text_field(self) -> TextField:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_text_field(self) -> TextField:
        return WindowsTextField()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()
    
    def create_text_field(self) -> TextField:
        return MacTextField()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

# Client code
def create_login_dialog(factory: UIFactory):
    button = factory.create_button()
    text_field = factory.create_text_field()
    checkbox = factory.create_checkbox()
    
    return {
        'button': button.render(),
        'text_field': text_field.render(),
        'checkbox': checkbox.render()
    }

# Usage
windows_ui = create_login_dialog(WindowsFactory())
mac_ui = create_login_dialog(MacFactory())
```

### Builder Pattern

```python
from typing import Optional, List, Any
from datetime import datetime

class Pizza:
    def __init__(self):
        self.size: str = ""
        self.crust: str = ""
        self.toppings: List[str] = []
        self.extra_cheese: bool = False
        self.cooking_time: Optional[int] = None
    
    def __str__(self):
        return (f"Pizza(size={self.size}, crust={self.crust}, "
                f"toppings={self.toppings}, cheese={self.extra_cheese})")

class PizzaBuilder:
    """Builder for Pizza objects"""
    
    def __init__(self):
        self._pizza = Pizza()
    
    def set_size(self, size: str) -> 'PizzaBuilder':
        if size not in ['small', 'medium', 'large']:
            raise ValueError("Invalid size")
        self._pizza.size = size
        return self
    
    def set_crust(self, crust: str) -> 'PizzaBuilder':
        if crust not in ['thin', 'thick', 'stuffed']:
            raise ValueError("Invalid crust")
        self._pizza.crust = crust
        return self
    
    def add_topping(self, topping: str) -> 'PizzaBuilder':
        self._pizza.toppings.append(topping)
        return self
    
    def add_toppings(self, toppings: List[str]) -> 'PizzaBuilder':
        self._pizza.toppings.extend(toppings)
        return self
    
    def add_extra_cheese(self) -> 'PizzaBuilder':
        self._pizza.extra_cheese = True
        return self
    
    def set_cooking_time(self, minutes: int) -> 'PizzaBuilder':
        self._pizza.cooking_time = minutes
        return self
    
    def build(self) -> Pizza:
        # Validation
        if not self._pizza.size:
            raise ValueError("Pizza size is required")
        if not self._pizza.crust:
            raise ValueError("Pizza crust is required")
        
        pizza = self._pizza
        self._pizza = Pizza()  # Reset for next build
        return pizza

class Director:
    """Optional director for predefined recipes"""
    
    def __init__(self, builder: PizzaBuilder):
        self._builder = builder
    
    def make_margherita(self) -> Pizza:
        return (self._builder
            .set_size('medium')
            .set_crust('thin')
            .add_toppings(['tomato sauce', 'mozzarella', 'basil'])
            .set_cooking_time(12)
            .build())
    
    def make_meat_lovers(self) -> Pizza:
        return (self._builder
            .set_size('large')
            .set_crust('thick')
            .add_toppings(['pepperoni', 'sausage', 'bacon', 'ham'])
            .add_extra_cheese()
            .set_cooking_time(15)
            .build())

# Usage
pizza = (PizzaBuilder()
    .set_size('large')
    .set_crust('thick')
    .add_topping('pepperoni')
    .add_topping('mushrooms')
    .add_extra_cheese()
    .build())

director = Director(PizzaBuilder())
margherita = director.make_margherita()
```

### Singleton Pattern

```python
import threading
from typing import Optional, Any

class SingletonMeta(type):
    """Thread-safe singleton using metaclass"""
    _instances: dict = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    """Database connection singleton"""
    
    def __init__(self):
        self._connected = False
        self._connection_string: str = ""
    
    def connect(self, connection_string: str):
        if self._connected:
            return
        
        # Simulate connection
        self._connection_string = connection_string
        self._connected = True
        print(f"Connected to: {connection_string}")
    
    def query(self, sql: str):
        if not self._connected:
            raise RuntimeError("Not connected to database")
        print(f"Executing: {sql}")
        return []
    
    @property
    def is_connected(self) -> bool:
        return self._connected

# Alternative: Decorator-based singleton
def singleton_decorator(cls):
    """Decorator for creating singletons"""
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton_decorator
class ConfigurationManager:
    def __init__(self):
        self._config = {}
    
    def set(self, key: str, value: Any):
        self._config[key] = value
    
    def get(self, key: str, default=None):
        return self._config.get(key, default)
```

### Prototype Pattern

```python
from copy import deepcopy
from typing import Dict, Any

class Prototype(ABC):
    """Base class for prototype pattern"""
    
    @abstractmethod
    def clone(self) -> 'Prototype':
        pass

class Document(Prototype):
    def __init__(self, title: str = "", content: str = ""):
        self.title = title
        self.content = content
        self.metadata: Dict[str, Any] = {}
        self.created_at: str = ""
        self.modified_at: str = ""
    
    def clone(self) -> 'Document':
        """Create deep copy of document"""
        return deepcopy(self)
    
    def __str__(self):
        return f"Document(title={self.title}, content={self.content[:30]}...)"

class DocumentRegistry:
    """Registry for document templates"""
    
    def __init__(self):
        self._prototypes: Dict[str, Document] = {}
    
    def register(self, key: str, document: Document):
        self._prototypes[key] = document
    
    def get(self, key: str) -> Document:
        if key not in self._prototypes:
            raise KeyError(f"Prototype '{key}' not found")
        return self._prototypes[key].clone()
    
    def create_from_template(self, key: str, **overrides) -> Document:
        doc = self.get(key)
        for key, value in overrides.items():
            setattr(doc, key, value)
        return doc

# Usage
registry = DocumentRegistry()

# Register templates
resume = Document(title="Resume", content="[Resume content]...")
resume.metadata = {'type': 'employment', 'pages': 1}
registry.register('resume', resume)

letter = Document(title="Cover Letter", content="[Letter content]...")
letter.metadata = {'type': 'employment', 'pages': 1}
registry.register('cover_letter', letter)

# Create instances from templates
my_resume = registry.create_from_template(
    'resume', 
    title="John Doe Resume",
    content="[John's specific resume content]"
)
```

-----

## Structural Patterns

### Adapter Pattern

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

# Legacy system
class LegacyPaymentSystem:
    def process_payment(self, amount: float, currency: str) -> str:
        # Old API
        return f"Legacy payment: {amount} {currency}"
    
    def refund_payment(self, transaction_id: str) -> str:
        return f"Refunded: {transaction_id}"

# New interface we want
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str, customer_id: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def refund(self, charge_id: str, amount: float) -> Dict[str, Any]:
        pass

# Adapter
class LegacyPaymentAdapter(PaymentProcessor):
    def __init__(self, legacy_system: LegacyPaymentSystem):
        self._legacy = legacy_system
    
    def charge(self, amount: float, currency: str, customer_id: str) -> Dict[str, Any]:
        result = self._legacy.process_payment(amount, currency)
        return {
            'success': True,
            'charge_id': f"ch_{hash(result) % 1000000}",
            'amount': amount,
            'currency': currency,
            'customer_id': customer_id,
            'raw_response': result
        }
    
    def refund(self, charge_id: str, amount: float) -> Dict[str, Any]:
        result = self._legacy.refund_payment(charge_id)
        return {
            'success': True,
            'refund_id': f"rf_{hash(result) % 1000000}",
            'charge_id': charge_id,
            'amount': amount,
            'raw_response': result
        }

# Two-way adapter
class NewToLegacyAdapter(LegacyPaymentSystem):
    def __init__(self, new_processor: PaymentProcessor):
        self._new = new_processor
    
    def process_payment(self, amount: float, currency: str) -> str:
        result = self._new.charge(amount, currency, "anonymous")
        return f"Processed: {result['charge_id']}"
    
    def refund_payment(self, transaction_id: str) -> str:
        result = self._new.refund(transaction_id, 0.0)
        return f"Refunded: {result['refund_id']}"
```

### Decorator Pattern

```python
from abc import ABC, abstractmethod
from typing import Optional, Callable
import time

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass

class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.00
    
    def description(self) -> str:
        return "Coffee"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()
    
    def description(self) -> str:
        return self._coffee.description()

class Milk(CoffeeDecorator):
    def __init__(self, coffee: Coffee):
        super().__init__(coffee)
    
    def cost(self) -> float:
        return self._coffee.cost() + 0.50
    
    def description(self) -> str:
        return f"{self._coffee.description()}, Milk"

class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.25
    
    def description(self) -> str:
        return f"{self._coffee.description()}, Sugar"

class WhippedCream(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.75
    
    def description(self) -> str:
        return f"{self._coffee.description()}, Whipped Cream"

class CaramelSyrup(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.60
    
    def description(self) -> str:
        return f"{self._coffee.description()}, Caramel"

# Functional decorator
def logging_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

def timing_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timing_decorator
@logging_decorator
def slow_operation():
    time.sleep(0.1)
    return "Done"
```

### Facade Pattern

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class CPU:
    def freeze(self):
        print("CPU: Freezing processor")
    
    def jump(self, position: int):
        print(f"CPU: Jumping to position {position}")
    
    def execute(self):
        print("CPU: Executing instructions")

class Memory:
    def load(self, position: int, data: bytes):
        print(f"Memory: Loading {len(data)} bytes at position {position}")
    
    def read(self, position: int, size: int) -> bytes:
        print(f"Memory: Reading {size} bytes from position {position}")
        return b"mock data"

class HardDrive:
    def read(self, sector: int, size: int) -> bytes:
        print(f"HardDrive: Reading {size} bytes from sector {sector}")
        return b"boot sector data"

class Display:
    def initialize(self):
        print("Display: Initializing")
    
    def show(self, data: str):
        print(f"Display: Showing {data}")

# Facade
class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
        self.display = Display()
    
    def start(self):
        print("=== Starting Computer ===")
        self.cpu.freeze()
        
        boot_sector = self.hard_drive.read(0, 512)
        self.memory.load(0, boot_sector)
        
        self.cpu.jump(0)
        self.cpu.execute()
        self.display.initialize()
        print("=== Computer Started ===")
    
    def shutdown(self):
        print("=== Shutting Down ===")
        self.display.show("Goodbye")
        self.cpu.freeze()
        print("=== Computer Off ===")

# Usage - simple interface for complex subsystem
computer = ComputerFacade()
computer.start()
computer.shutdown()
```

### Proxy Pattern

```python
from abc import ABC, abstractmethod
from typing import Any
import time

class ExpensiveResource(ABC):
    @abstractmethod
    def get_data(self, key: str) -> Any:
        pass

class RealExpensiveResource(ExpensiveResource):
    """The actual expensive resource"""
    
    def __init__(self):
        self._data = {str(i): f"data_{i}" for i in range(1000)}
        # Simulate slow initialization
        time.sleep(0.1)
    
    def get_data(self, key: str) -> Any:
        # Simulate expensive operation
        time.sleep(0.01)
        return self._data.get(key)

class CachingProxy(ExpensiveResource):
    """Proxy that caches results"""
    
    def __init__(self):
        self._real = RealExpensiveResource()
        self._cache: Dict[str, Any] = {}
    
    def get_data(self, key: str) -> Any:
        if key in self._cache:
            print(f"Proxy: Cache hit for {key}")
            return self._cache[key]
        
        print(f"Proxy: Cache miss for {key}")
        result = self._real.get_data(key)
        self._cache[key] = result
        return result

class VirtualProxy(ExpensiveResource):
    """Proxy that creates real object on demand"""
    
    def __init__(self):
        self._real: RealExpensiveResource = None
    
    def _get_real(self) -> RealExpensiveResource:
        if self._real is None:
            print("VirtualProxy: Creating real object")
            self._real = RealExpensiveResource()
        return self._real
    
    def get_data(self, key: str) -> Any:
        return self._get_real().get_data(key)

class ProtectionProxy(ExpensiveResource):
    """Proxy that controls access to real object"""
    
    def __init__(self, user_roles: List[str]):
        self._real = RealExpensiveResource()
        self._allowed_roles = ['admin', 'user']
        self._user_roles = user_roles
    
    def get_data(self, key: str) -> Any:
        if not any(role in self._allowed_roles for role in self._user_roles):
            raise PermissionError(f"Access denied. Required roles: {self._allowed_roles}")
        return self._real.get_data(key)
```

-----

## Behavioral Patterns

### Observer Pattern

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import threading

class Observer(ABC):
    @abstractmethod
    def update(self, event: Dict[str, Any]):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()
    
    def attach(self, observer: Observer):
        with self._lock:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        with self._lock:
            self._observers.remove(observer)
    
    def notify(self, event: Dict[str, Any]):
        with self._lock:
            for observer in self._observers:
                observer.update(event)

class NewsAgency(Subject):
    def __init__(self):
        super().__init__()
        self._latest_news: str = ""
    
    def publish_news(self, news: str):
        self._latest_news = news
        self.notify({
            'type': 'news',
            'content': news,
            'timestamp': datetime.now().isoformat()
        })
    
    @property
    def latest_news(self) -> str:
        return self._latest_news

class NewsChannel(Observer):
    def __init__(self, name: str):
        self.name = name
        self.received_news: List[Dict[str, Any]] = []
    
    def update(self, event: Dict[str, Any]):
        self.received_news.append(event)
        print(f"{self.name} received: {event['content']}")

class EmailSubscriber(Observer):
    def __init__(self, email: str):
        self.email = email
    
    def update(self, event: Dict[str, Any]):
        print(f"Email to {self.email}: {event['content']}")

# Usage
agency = NewsAgency()
cnn = NewsChannel("CNN")
bbc = NewsChannel("BBC")
subscriber = EmailSubscriber("user@example.com")

agency.attach(cnn)
agency.attach(bbc)
agency.attach(subscriber)

agency.publish_news("Breaking: AI advances in 2024")
```

### Strategy Pattern

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import random

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[Any]) -> List[Any]:
        pass

class QuickSort(SortStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSort(SortStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)
    
    def _merge(self, left: List, right: List) -> List:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class RandomSort(SortStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        shuffled = data.copy()
        random.shuffle(shuffled)
        return shuffled

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data: List[Any]) -> List[Any]:
        return self._strategy.sort(data)

# Usage
data = [64, 34, 25, 12, 22, 11, 90]
sorter = Sorter(QuickSort())
print(sorter.sort(data))

sorter.set_strategy(MergeSort())
print(sorter.sort(data))
```

### Command Pattern

```python
from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Any
from datetime import datetime

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass
    
    @abstractmethod
    def redo(self):
        pass

class TextEditor:
    def __init__(self):
        self._content: str = ""
        self._clipboard: str = ""
    
    def insert_text(self, text: str, position: int):
        self._content = self._content[:position] + text + self._content[position:]
    
    def delete_text(self, start: int, end: int):
        deleted = self._content[start:end]
        self._content = self._content[:start] + self._content[end:]
        return deleted
    
    @property
    def content(self) -> str:
        return self._content
    
    def set_content(self, content: str):
        self._content = content
    
    def copy(self, start: int, end: int):
        self._clipboard = self._content[start:end]
    
    def paste(self, position: int):
        self.insert_text(self._clipboard, position)

class InsertCommand(Command):
    def __init__(self, editor: TextEditor, text: str, position: int):
        self.editor = editor
        self.text = text
        self.position = position
    
    def execute(self):
        self.editor.insert_text(self.text, self.position)
    
    def undo(self):
        self.editor.delete_text(self.position, self.position + len(self.text))
    
    def redo(self):
        self.execute()

class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, start: int, end: int):
        self.editor = editor
        self.start = start
        self.end = end
        self.deleted_text: str = ""
    
    def execute(self):
        self.deleted_text = self.editor.delete_text(self.start, self.end)
    
    def undo(self):
        self.editor.insert_text(self.deleted_text, self.start)
    
    def redo(self):
        self.execute()

class CommandManager:
    def __init__(self):
        self._history: List[Command] = []
        self._current: int = -1
    
    def execute(self, command: Command):
        command.execute()
        self._history = self._history[:self._current + 1]
        self._history.append(command)
        self._current += 1
    
    def undo(self):
        if self._current >= 0:
            command = self._history[self._current]
            command.undo()
            self._current -= 1
    
    def redo(self):
        if self._current < len(self._history) - 1:
            self._current += 1
            command = self._history[self._current]
            command.redo()
    
    def can_undo(self) -> bool:
        return self._current >= 0
    
    def can_redo(self) -> bool:
        return self._current < len(self._history) - 1
```

### State Pattern

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class State(ABC):
    @abstractmethod
    def insert_coin(self, machine: 'VendingMachine'):
        pass
    
    @abstractmethod
    def eject_coin(self, machine: 'VendingMachine'):
        pass
    
    @abstractmethod
    def select_product(self, machine: 'VendingMachine', product: str):
        pass
    
    @abstractmethod
    def dispense(self, machine: 'VendingMachine'):
        pass

class VendingMachine:
    def __init__(self):
        self._state: State = NoCoinState()
        self._products: Dict[str, int] = {'cola': 5, 'chips': 5, 'candy': 5}
        self._coin_inserted: float = 0.0
        self._selected_product: str = ""
    
    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, state: State):
        self._state = state
    
    def insert_coin(self, amount: float):
        self._state.insert_coin(self)
    
    def eject_coin(self):
        self._state.eject_coin(self)
    
    def select_product(self, product: str):
        self._state.select_product(self, product)
    
    def dispense(self):
        self._state.dispense(self)

class NoCoinState(State):
    def insert_coin(self, machine: VendingMachine):
        machine._coin_inserted = 0.50
        machine.state = HasCoinState()
        print("Coin inserted")
    
    def eject_coin(self):
        print("No coin to return")
    
    def select_product(self, machine: VendingMachine, product: str):
        print("Please insert coin first")
    
    def dispense(self, machine: VendingMachine):
        print("Please insert coin first")

class HasCoinState(State):
    def insert_coin(self, machine: VendingMachine):
        print("Coin already inserted")
    
    def eject_coin(self, machine: VendingMachine):
        machine._coin_inserted = 0.0
        machine.state = NoCoinState()
        print("Coin returned")
    
    def select_product(self, machine: VendingMachine, product: str):
        if product not in machine._products:
            print(f"Product {product} not available")
            return
        if machine._products[product] <= 0:
            print(f"Product {product} out of stock")
            return
        
        machine._selected_product = product
        machine.state = ProductSelectedState()
        print(f"Product {product} selected")
    
    def dispense(self, machine: VendingMachine):
        print("Please select a product")

class ProductSelectedState(State):
    def insert_coin(self, machine: VendingMachine):
        print("Product already selected")
    
    def eject_coin(self, machine: VendingMachine):
        machine._coin_inserted = 0.0
        machine._selected_product = ""
        machine.state = NoCoinState()
        print("Coin returned, selection cancelled")
    
    def select_product(self, machine: VendingMachine, product: str):
        print(f"Already selected {machine._selected_product}")
    
    def dispense(self, machine: VendingMachine):
        machine._products[machine._selected_product] -= 1
        machine._coin_inserted = 0.0
        machine._selected_product = ""
        machine.state = NoCoinState()
        print("Product dispensed!")
```

-----

## Anti-Patterns to Avoid

| Anti-Pattern | Description | Solution |
|--------------|-------------|----------|
| **God Class** | Single class controlling everything | Split into focused classes |
| **Spaghetti Code** | Unstructured, tangled code | Refactor to clear structure |
| **Copy-Paste Programming** | Duplicating code | Create abstractions |
| **Premature Optimization** | Optimizing before needed | Profile first, optimize later |
| **Golden Hammer** | One solution for all problems | Use appropriate tools |
| **Not Invented Here** | Avoiding existing solutions | Evaluate objectively |
| **Analysis Paralysis** | Over-planning, no action | Iterate and adapt |
| **Magic Numbers** | Unnamed constants | Use named constants |
