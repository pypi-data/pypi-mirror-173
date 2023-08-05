import json, time, traceback
import datetime
from datetime import timedelta
# MQ utilities package
from mpsmqutils import mqutils
# Job tracker module
from mpsjobtracker.trackers.jobtracker import JobTracker, log_error_and_reraise

job_tracker = JobTracker()

class JobMonitor():
    def __init__(self, progress_check_duration):
        self.progress_check_duration = timedelta(seconds=progress_check_duration)

    def run(self):
        while True:
            self.check_inprocess_jobs()
            time.sleep(self.progress_check_duration.seconds)


    def check_inprocess_jobs(self):
        current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0)
        inprocess_jobs = job_tracker.get_jobs('running')
        print('Checking inprocess jobs ' + str(current_time), flush=True)

        for job_doc in inprocess_jobs:
            check_time = True
            job_id = job_doc["_id"]
            print(f"inprocess job {str(job_id)}", flush=True)
            parent_ref = job_doc.get('parent_ref')
            if (parent_ref is not None):
                print(f'parent ticket id {parent_ref}', flush=True)
            else:
                # Check if this job is complete by seeing if all child jobs are failed or successful
                print("Attempting to resolve parent job " + str(job_id), flush=True)
                print(len(list(child_jobs)))
                child_jobs = job_tracker.get_child_jobs(job_id)
                job_finished = True
                for child_job in child_jobs:
                    print(str(child_job))
                    child_job_status = child_job['job_management']['job_status']
                    print(child_job_status)
                    if child_job_status != 'success' and child_job_status != 'failed':
                        job_finished = False

                if job_finished and len(list(child_jobs)) > 0:
                    print("Found and a complete job...", flush=True)
                    job_tracker.set_job_status('success', job_id)
                    print("Resolved the completed job...", flush=True)
                    # We skip the time comparison if we resolve a job
                    check_time = False
                    # DROP SOMETHING ON A SUCCESS QUEUE
                else:
                    print("Job is not finished...")

            try:
                job_doc_time = job_doc['last_modified_date'].replace(tzinfo=datetime.timezone.utc)
                diff = current_time - job_doc_time
                #If it has been more than the expected duration, we assume
                #that the process has stalled.
                if check_time and diff >= self.progress_check_duration:
                    self.handle_stalled_job(job_doc)
            except Exception as e:
                print('exception: {}'.format(e))


    def handle_stalled_job(self, job_doc):
        job_management = job_doc.get("job_management")
        if (job_management is None):
            #TODO what to do here - what does this mean?
            return False
        number_of_tries = job_management["numberOfTries"]
        max_number_of_tries = job_management["maxNumberOfTries"]
        if (number_of_tries < max_number_of_tries):
            #Requeue
            print("Requeued job id" + str(job_doc["_id"]))
            return self.requeue(job_doc, number_of_tries+1)
        #Trigger the undo procedure.
        return self.revert(job_doc)

    def requeue(self, job_doc, trial_number):
        #Update the number of tries in the tracker file
        job_doc["job_management"]["numberOfTries"] = trial_number
        try:
            updated_job_doc = job_tracker.replace_tracker_doc(job_doc)
        except Exception as e:
            #TODO what to do here - what does this mean if the tracker retrievel fails?
            return False
        #Log message
        #Queue the step again
        ticket_id = str(job_doc['_id'])
        parent_ticket_id = str(job_doc.get('parent_ref', ''))
        if not parent_ticket_id:
            message = mqutils.create_task_manager_queue_message(ticket_id)
        else:
            message = mqutils.create_requeue_message(ticket_id, parent_ticket_id)
        try:
            json_message = json.loads(message)
        except ValueError as e:
            log_error_and_reraise("JSON loading failed in requeue")
        job_name = json_message["event"]
        mqconn = mqutils.get_mq_connection()
        queue = '/queue/'+job_name
        mqconn.send(queue, message,  headers = {"persistent":"true"})
        return True

    def revert(self, job_doc):
        #Nothing to revert if this is the task manager
        if job_doc.get('parent_ref') is None:
            return True
        ticket_id = str(job_doc['_id'])
        parent_ticket_id = str(job_doc.get('parent_ref', ''))
        message = mqutils.create_revert_message(ticket_id, parent_ticket_id)
        if (message is None):
            #TODO Do something that indicates there are no more tasks to revert
            return True
        try:
            json_message = json.loads(message)
        except ValueError as e:
            log_error_and_reraise("JSON loading failed in revert")


        job_name = json_message["event"]

        #Update the number of tries in the tracker file
