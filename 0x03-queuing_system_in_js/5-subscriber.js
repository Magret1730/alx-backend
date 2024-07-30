import redis from 'redis';

const client = redis.createClient();

client.on('connect', function() {
	console.log('Redis client connected to the server');
});

client.on('error', (err) => {
	console.log(`Redis client not connected to the server: ${err}`);
});

// Duplicate the client for subscribing to channels
const subscriber = client.duplicate();

// Handle successful connection for the subscriber
subscriber.on('connect', function () {
	console.log('Redis client connected to the server');
});

// Handle connection errors for the subscriber
subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Subscribe to the 'holberton school channel'
subscriber.subscribe('holberton school channel');

// Handle messages received on the subscribed channel
subscriber.on('message', (channel, message) => {
  console.log(`Received message: ${message} on channel: ${channel}`);
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe('holberton school channel');
    subscriber.quit();
  }
});
