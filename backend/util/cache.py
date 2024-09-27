import redis

class RedisCache:
    _instance = None

    """
    Ensures that only a single instance of the `RedisCache` class is created.
    
    This method is used to implement the Singleton pattern for the `RedisCache` class.
    It checks if an instance of the class already exists, and if not, it creates a new instance.
    The created instance is stored in the `_instance` class attribute, and subsequent calls to
    this method will return the same instance.
    """
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance


    """
    Ensures only one instance of the `RedisCache` class is created and implements the Singleton pattern.
        
    Checks if an instance already exists; if not, creates a new instance stored in the `_instance` attribute.
    Subsequent calls return the same instance.
        
    Methods:
    - `initialize`: Initializes the Redis client with specified host, port, and database.
    - `get_instance`: Returns the Redis client instance.
    """
    @classmethod
    def initialize(cls, host='localhost', port=6379, db=0):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        cls._instance.client = redis.Redis(host=host, port=port, db=db)

    """
    Ensures that a valid Redis client instance is returned.

    Raises an exception if the Redis cache has not been initialized by calling `RedisCache.initialize()` first.
    Returns the Redis client instance stored in the `_instance` attribute of the `RedisCache` class.
    """
    @classmethod
    def get_instance(cls):
        if cls._instance is None or cls._instance.client is None:
            raise Exception("Redis cache has not been initialized. Call RedisCache.initialize() first.")
        return cls._instance.client


"""
Returns the singleton instance of the Redis client.

This function provides access to the Redis client instance managed by the `RedisCache` class.
It ensures that the Redis cache has been properly initialized by calling `RedisCache.initialize()`
before returning the client instance.

Raises:
    Exception: If the Redis cache has not been initialized.

Returns:
    redis.Redis: The singleton instance of the Redis client.
"""
def get_redis_client():
        return RedisCache.get_instance()
