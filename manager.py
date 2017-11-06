from app import resolver, nautilus
from capitains_nautilus.manager import FlaskNautilusManager

manager = FlaskNautilusManager(resolver, nautilus)

if __name__ == "__main__":
    manager()
