const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

const app = express();
const client = redis.createClient();

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

let availableSeats = 50;
let reservationEnabled = true;

async function reserveSeat(number) {
	await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
	const seats = await getAsync('available_seats');
	return Number(seats);
}

const queue = kue.createQueue();

app.get('/available_seats', async (req, res) => {
	res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', async (req, res) => {
	if (!reservationEnabled) {
		res.json({ status: 'Reservation are blocked' });
		return;
	}

	const job = queue.create('reserve_seat');
	job.save((err) => {

		if (err) {
			res.json({ status: 'Reservation Failed' });
		} else {
			res.json({ status: 'Reservation in process' });
		}
	});
});

app.get('/process', async (req, res) => {
	res.json({ status: 'Queue processing' });

	queue.process('reserve_seat', async (job, done) => {
		try {
			const currentSeats = await getCurrentAvailableSeats();
			if (currentSeats <= 0) {
				reservationEnabled = false;
				done(new Error('Not enough seats available'));
				return;
			}

			availableSeats--;
			await reserveSeat(availableSeats);

			if (availableSeats === 0) {
				reservationEnabled = false;
			}

			done();
			console.log(`Seat reservation job ${job.id} completed`);
		} catch (error) {
			done(error);
			console.log(`Seat reservation job ${job.id} failed: {error.message}`);
		}
	});
});

const PORT = 1245;
app.listen(PORT, () => {
	console.log(`Server is running on port ${PORT}`);
});
