import queue
import threading


class jobQuery:
    def __init__(self, link_to_job, html_content):
        self._link_to_job = link_to_job
        self._html_content = html_content


class jobsManager:
    def __init__(self):
        self.jobs_q = queue.Queue()
        self.jobs_thread = threading.Thread()

    def add_job(self, job: jobQuery):
        self.jobs_q.put(job)

    def run(self):
        while True:
            try:
                job = self.jobs_q.get(block=True, timeout=5)

            except:
                continue
