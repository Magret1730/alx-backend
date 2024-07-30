import redis from 'redis';

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

function displaySchoolValue (schoolName) {
	client.get(schoolName, function(err, result) {
		if (err) {
			console.error(err);
		} else {
			console.log(result);
		};
	});
};

// redisConnect().catch(err => console.error('Failed to connect:', err));
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
