import redis
from config import settings


def create_redis_client():
    """
    Creates and tests a synchronous Redis client instance for Flask-Session.
    """
    try:
        # 1. Create the SYNCHRONOUS client instance
        client = redis.Redis(
            # Use the correct settings for REDIS, not Flask
            host=settings.redis_host, 
            port=settings.redis_port,
            db=1,  # Using a separate DB (like 1) for sessions is good practice
        )
        
        # 2. Test the connection immediately on startup
        client.ping()
        
        print(f"Flask-Session: Successfully connected to Redis at {settings.redis_host}:{settings.redis_port}")
        return client

    except redis.exceptions.ConnectionError as e:
        print("="*50)
        print(f"FLASK-SESSION CRITICAL ERROR: Could not connect to Redis.")
        print(f"Make sure REDIS_HOST='{settings.redis_host}' and REDIS_PORT='{settings.redis_port}' are correct in your .env file.")
        print(f"(If Redis is on your host, use REDIS_HOST=host.docker.internal)")
        print(f"Error: {e}")
        print("="*50)
    except AttributeError:
        print("="*50)
        print(f"FLASK-SESSION CRITICAL ERROR: 'settings' object is missing 'redis_host' or 'redis_port'.")
        print("Please add REDIS_HOST and REDIS_PORT to your .env file and settings.py")
        print("="*50)
    
    # This allows the app to start, but sessions will fail
    return None

# This is the file your Flask app (app.py) is looking for.
# It creates one, synchronous client instance by calling the function.
RedisClient = create_redis_client()