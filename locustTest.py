from locust import HttpLocust,TaskSet,task


class Userbehavior(TaskSet):

    @task
    def baidu_index(self):
        self.client("/")

class WebsitUser(HttpLocust):
    task_set = Userbehavior
    min_wait = 3000
    max_wait = 6000