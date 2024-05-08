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

		expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
		expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);

		expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
		expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);

		expect(consoleSpy.calledWith(`Notification job created: ${queue.testMode.jobs[0].id}`)).to.be.true;
					expect(consoleSpy.calledWith(`Notification job created: ${queue.testMode.jobs[0].id}`)).to.be.true
	});
});
