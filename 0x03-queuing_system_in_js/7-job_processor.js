import kue from 'kue';

// Blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send notification
function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100); // Track job progress

  if (blacklistedNumbers.includes(phoneNumber)) {
    done(new Error(`Phone number ${phoneNumber} is blacklisted`)); // Fails the job if phone number is blacklisted
    return;
  }

  job.progress(50, 100); // Track job progress to 50%
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  done(); // Complete the job successfully
}

// Create a Kue queue
const queue = kue.createQueue();

// Process jobs from the push_notification_code_2 queue
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
