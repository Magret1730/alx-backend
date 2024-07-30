import kue from 'kue';

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153538781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4159518782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account'
  }
];


const queue = kue.createQueue();

const job = jobs.forEach((new_job) => {
	// Create a job with the object data
	const job = queue.create("push_notification_code_2", new_job)
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
	job.on('progress', (progress) => {
    	console.log(`Notification job ${job.id} ${progress}% complete`);
	});
});
