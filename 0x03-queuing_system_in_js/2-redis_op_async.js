import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('connect', () => {
	console.log('Redis client connected to the server');
});

client.on('error', (error) => {
	console.error(`Redis client not connected to the server: ${error}`);
});

function setNewSchool(schoolName, value) {
	client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName) {
	const getAsync = promisify(client.get).bind(client);
	try {
		const value = await getAsync(schoolName);
		console.log(value);
	} catch (error) {
		console.error(`Error retrieving value for ${schoolName}: ${error}`);
	}
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
