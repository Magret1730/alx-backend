import createPushNotificationsJobs from './8-job.js';
import kue from 'kue';
const sinon = require('sinon');
const { expect } = require('chai');

const queue = kue.createQueue();

before(function() {
  queue.testMode.enter();
});

afterEach(function() {
  queue.testMode.clear();
});

after(function() {
  queue.testMode.exit()
});

describe ('createPushNotificationsJobs', () => {
	it(('should display an error message if the jobs is not an array'), function() {
		expect(() => createPushNotificationsJobs('not an array', queue)).to.throw('Jobs is not an array');
	});

	it (('should test correct job creations and type'), function() {
		const jobs = [
  				{
					phoneNumber: '4153518780',
    					message: 'This is the code 1234 to verify your account'
  				},
  				{
	    				phoneNumber: '4153518781',
    					message: 'This is the code 4562 to verify your account'
  				}
			]

		createPushNotificationsJobs(jobs, queue);
		// console.log(queue.testMode.jobs[0]);
		expect(queue.testMode.jobs.length).to.equal(2);
		expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
		expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
		expect(queue.testMode.jobs[0].data).to.eql({
			phoneNumber: '4153518780',
                        message: 'This is the code 1234 to verify your account'
		});
		expect(queue.testMode.jobs[1].data).to.eql({
			phoneNumber: '4153518781',
                        message: 'This is the code 4562 to verify your account'
		});
	});

	it('should log events for job lifecycle', function(done) {
		const jobs = [{
        		phoneNumber: '4153518780',
        		message: 'This is the code 1234 to verify your account'
     		}];

    		const consoleSpy = sinon.spy(console, 'log');

    		createPushNotificationsJobs(jobs, queue);

    		const job = queue.testMode.jobs[0];
    		job.emit('complete');
    		job.emit('failed', new Error('Error'));
    		job.emit('progress', 50);

	    expect(consoleSpy.calledWith(`Notification job created: ${job.id}`)).to.be.true;
    	    expect(consoleSpy.calledWith(`Notification job ${job.id} completed`)).to.be.true;
    	    // expect(consoleSpy.calledWith(`Notification job ${job.id} failed: Error`)).to.be.true;
	    expect(consoleSpy.calledWith(`Notification job ${job.id} 50% complete`)).to.be.true;

	    consoleSpy.restore();
    	    done();
	});
});
