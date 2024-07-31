// import kue from 'kue';
// const queue = kue.createQueue();

function createPushNotificationsJobs(jobs, queue) {
	if (!Array.isArray(jobs)) {
		// console.log('Jobs is not an array');
		throw new Error('Jobs is not an array');
	}

	jobs.forEach((new_job) => {
        const job = queue.create("push_notification_code_3", new_job);

		// Check if job is created properly
        	// if (!job) {
            	// console.error('Failed to create job');
            	// return;
        	// }

		job.save((err) => {
                if (!err) {
                    console.log(`Notification job created: ${job.id}`);

                    // Event listeners for the job
                    job.on("complete", () => {
                        console.log(`Notification job ${job.id} completed`);
                    });

                    job.on("failed", (err) => {
                        console.log(`Notification job ${job.id} failed: ${err}`);
                    });

                    job.on('progress', (progress) => {
                        console.log(`Notification job ${job.id} ${progress}% complete`);
                    });
                }
            });
    });
}

export default createPushNotificationsJobs;
