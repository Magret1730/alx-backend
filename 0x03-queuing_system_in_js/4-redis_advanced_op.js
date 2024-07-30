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

client.hset('HolbertonSchools', 'Portland', 50, redis.print);
client.hset('HolbertonSchools', 'Seattle', 80, redis.print);
client.hset('HolbertonSchools', 'New York', 20, redis.print);
client.hset('HolbertonSchools', 'Bogota', 20, redis.print);
client.hset('HolbertonSchools', 'Cali', 40, redis.print);
client.hset('HolbertonSchools', 'Paris', 2, redis.print);

const getAll = client.hgetall('HolbertonSchools', function (err, response) {
	if (err) {
		console.log(err);
	} else {
		console.log(response);
	}
});

//let userSession = await client.hGetAll('user-session:123');
//console.log(JSON.stringify(userSession, null, 2));
