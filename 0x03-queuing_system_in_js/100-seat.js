import express from 'express';
import { createClient } from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;

// Initialize Redis client
const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Initialize Kue queue
const queue = kue.createQueue();

// Initialize variables
let reservationEnabled = true;

// Set initial available seats
const initialSeats = 50;
(async () => {
  await setAsync('available_seats', initialSeats);
})();

// Functions for Redis operations
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10);
}

// Express routes
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      const availableSeats = await getCurrentAvailableSeats();
      if (availableSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }

      await reserveSeat(availableSeats - 1);

      if (availableSeats - 1 === 0) {
        reservationEnabled = false;
      }

      done();
    } catch (error) {
      done(error);
    }
  });
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
