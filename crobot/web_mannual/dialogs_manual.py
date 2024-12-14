import requests
import time, os
import json
import Logger as log

work_dir = "/CLSRobot/crobot/web_mannual"
server_info = { "web_server":"127.0.0.1", "port":"5000" }
web_publish_info = { "web_server":"10.204.125.4", "port":"32778" } #This port is published by container
base_url = "http://{web_server}:{port}".format(**server_info)
create_step_url = "{}/create_step/".format(base_url)
query_url = "{}/query".format(base_url)
proxies = {"http":None, "https": None}

__all__ = ['pause_execution', 'start_web_service', 'stop_web_service']

step_info = {
        "message":"Test execution paused. Press OK to continue in URL:",
        "options":"Pass,Fail",
        "stepID": "T1_S1",
        "image":"",
        "description":"Here is the step tips."
        }

#Can't run well with robot now, please start the service alone
def start_web_service():
    cmd = "cd {};".format(work_dir)
    cmd += "export FLASK_APP=web.py; export FLASK_ENV=development; unset http_proxy;"
    cmd += "nohup flask run -h 0.0.0.0 -p {} > service.log 2>&1 &".format(server_info["port"])
    status = os.system(cmd)
    if status != 0:
        raise Exception("Start manual web service failed.")

def stop_web_service():
    return
    cmd = "pkill flask"
    status = os.system(cmd)
    if status != 0:
        raise Exception("Start manual web service failed.")

def query_data(URL):
    res = requests.get(URL, proxies=proxies)
    if res.status_code != 200:
        raise Exception("{}, fetch data failed: {}".format(res.status_code, URL))
    rows = res.json()
    return rows


def pause_execution(server_info=server_info, access_info=web_publish_info,
        step_info=step_info):
    """Pauses test execution until user clicks ``Ok`` button.
    """
    response_url = "http://{}:{}/confirm/{}".format(access_info["web_server"],
            access_info["port"], step_info["stepID"])
    MSG = "{}\n  {}".format(step_info["message"], response_url)
    create_step(step_info)
    log.info("Creating step is done")
    log.info(MSG)
    query_selected_url = "{}/{}".format(query_url, step_info["stepID"])
    while True:
        time.sleep(1)
        res = requests.get(query_selected_url, proxies=proxies)
        content = json.loads(res.content.decode().strip())[0]
        if res.status_code == 200 and content:
            if "fail" in content.lower():
                raise Exception("Failed option is selected")
            break


def create_step(step_info):
    res = requests.post(create_step_url, step_info, proxies=proxies)
    if res.status_code != 200:
        log.info('Opening: {}'.format(create_step_url))
        raise Exception("{}, fetch data failed: {}".format(res.status_code, create_step_url))

    
