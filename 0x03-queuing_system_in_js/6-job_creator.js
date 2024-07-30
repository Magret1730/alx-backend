import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Create an object containing the job data
const jobData = {
        phoneNumber: "012345678",
        message: "Test Notification",
};

// Create a job with the object data
const job = queue.create("push_notification_code", jobData)
	.save( function(err) {
	if (!err) {
		console.log(`Notification job created: ${job.id}`);
	}
});

// Event listeners for the job
job.on("complete", function() {
	console.log('Notification job completed');
});
job.on("failed", function() {
	console.log('Notification job failed');
});
