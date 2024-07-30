import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('connect', function() {
	console.log('Redis client connected to the server');
});

client.on('error', (err) => {
	console.log(`Redis client not connected to the server: ${err}`);
});

function setNewSchool (schoolName, value) {
	client.set(schoolName, value, redis.print);
	// redis.print(Reply: OK);
};

// Promisify makes us use async and await

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue (schoolName) {
	try {
		const result = await getAsync(schoolName);
		console.log(result);
	} catch (err) {
		console.error(err);
	}
};

// redisConnect().catch(err => console.error('Failed to connect:', err));
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
