import { expect } from 'chai';
import sinon from 'sinon';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
	let consoleSpy;
	let queue;

	beforeEach(() => {
		consoleSpy = sinon.spy(console, 'log');
		queue = createQueue({ name: 'push_notification_code_test', });
		queue.testMode.enter();
	});

	afterEach(() => {
		consoleSpy.restore();
		queue.testMode.clear();
		queue.testMode.exit();
	});

	it('displays an error message if jobs is not an array', () => {
		const invalidCall = () => createPushNotificationsJobs('invalid', queue);

		expect(invalidCall).to.throw('Jobs is not an array');
	});

	it('creates and adds jobs in the queue', () => {
		const jobDes = [
			{ phoneNumber: '4153518780', message: 'This is the code 1234' },
			{ phoneNumber: '4153518781', message: 'This is the code 5678' },
		];

		createPushNotificationsJobs(jobDes, queue);

		expect(queue.testMode.jobs.length).to.equal(jobDes.length);

		queue.testMode.jobs.forEach((job, index) => {
			expect(job.type).to.equal('push_notification_code_3');
			expect(job.data).to.deep.equal(jobDes[index]);
			job.emit('complete');
			expect(consoleSpy.calledWith(`Notification job ${job.id} completed`)).to.be.true;
		});
	});

	it('registers the progress event handler for a job', () => {
		const job = queue.createJob('push_notification_code_3', { phoneNumber: '1234567890', message: 'Test message' });
		job.save((error) => {
			if (error) {
				console.error(`Error saving job: ${error}`);
				done(error);
				return;
			}

			job.on('progress', (progress) => {
				expect(consoleSpy.calledWith(`Notification job ${job.id} ${progress}% complete`)).to.be.true;
				done();
			});
			job.emit('progress')
		});
	});

	it('registers the failed event handler for a job', () => {
		const job = queue.createJob('push_notification_code_3', { phoneNumber: '1234567890', message: 'Test message' });
		job.save((error) => {
			if (error) {
				console.error(`Error saving job: ${error}`);
				return;
			}

			job.on('failed', (errorMessage) => {
				expect(consoleSpy.calledWith(`Notification job ${job.id} failed: ${errorMessage.message}`)).to.be.true;
			});

			const errorMessage = new Error('Failed to send');
			job.emit('failed', errorMessage);
		});
	});
});
