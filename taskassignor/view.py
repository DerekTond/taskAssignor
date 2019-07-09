import json
from datetime import datetime
import logging

from flask import Blueprint
from flask import request
from flask import jsonify
from sqlalchemy import and_
import flask_restless

from taskassignor import db
from taskassignor.utils import str_encrypt, hash_id
from taskassignor.models import Task


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('output.log')
file_handler.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

view_bp = Blueprint('view',__name__)


# 路由函数
@view_bp.route('/assignor/new_task', methods=["POST"])
def new_task():
    """
    分发者提供单个任务，将任务存入数据库
    传入json格式为:
    {
        "assignor_id": <int>,
        "task_info": [
            {
                "id": <int>,
                "info": <str>
            }
        ]
    }
    :return: batch_id
    :rtype: int
    """
    try:
        all_info = request.get_data(as_text=True)
        all_info = json.loads(all_info)
        task_info = all_info['task_info']
        assignor_id = all_info['assignor_id']
        batch_id = str_encrypt(hash_id(assignor_id)) # batch_id为(分发者id+当前时间)的sha1
        for single_task in task_info:
            new_info = Task(batch_id=batch_id, id=single_task['id'], info=single_task['info'], status="unchecked")
            db.session.add(new_info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error("%s_exception|input = %s|exception=%s", new_task.__name__, all_info, e, exc_info=True)
        return jsonify({'status': 0, 'error': "wrong input"}), 404
    logger.info("%s_success|assignor_id=%s|batch_id=%s", new_task.__name__, assignor_id, batch_id)
    return jsonify({'status': 1, 'batch_id': batch_id}), 200


@view_bp.route("/checker/take_task", methods=["POST"])
def take_task():
    """
    如果数据库有待标定任务，标定者接受任务，得到json格式任务
    传入json格式为:
    {
        "checker_id": <int>
    }
    传出json格式为:
    {
        "checker_id": <int>,
        "task_info": [
            {
                "id": <int>,
                "info": <str>
            }
        ]
    }
    :return: 任务数据
    :rtype: json
    """
    try:
        all_info = json.loads(request.get_data(as_text=True))
        checker_id = all_info["checker_id"]
    except Exception as e:
        logger.error("%s_WrongInput|input = %s|exception=%s", new_task.__name__, all_info, e, exc_info=True)
        return jsonify({'status': 0, 'error': "wrong input"}), 404
    try:
        tasks = Task.query.filter(Task.checker==None).all()
        if tasks:
            checker_tasks = []
            tasks_nums = Task.query.filter(and_(Task.checker==checker_id,Task.status=="checking")).count()# 查任务
            for task in tasks:
                if tasks_nums >= 10:
                    break
                task.checker = checker_id
                task.time = datetime.utcnow()
                task.status = "checking"
                task_info = {"batch_id": task.batch_id, "r_id": task.r_id, "info": task.info}
                checker_tasks.append(task_info)
                tasks_nums += 1
                db.session.commit()
            logger.info("%s_success|checker_id=%s", take_task.__name__, checker_id)
            return jsonify({"status": 1, "checker_id": checker_id, "task_info": checker_tasks}), 200
        else:
            logger.info("%s_failed|checker_id=%s", take_task.__name__, checker_id)
            return jsonify({"status": 0, "task_info": "no more task"}), 404
    except Exception as e:
        logger.error("%s_WrongDataBase|input = %s|exception=%s", take_task.__name__, e, exc_info=True)
        return jsonify({"status":2, "message":"the I/O of database is breakdown"})


# @view_bp.route("/checker/submit", methods=["POST"])
# def submit():
#     """
#     如果数据库有待标定任务，标定者接受任务，得到json格式任务
#     传入json格式为:
#     {
#         "checker_id": <int>,
#         "r_id":<int>,
#         "checked_info":<str>
#     }
#     传出json格式为:
#     {
#         "status": <int>,
#         "message":"str"
#     }
#     :return: 任务数据
#     :rtype: json
#     """
#     try:
#         all_info = json.loads(request.get_data(as_text=True))
#         checker_id = all_info['checker_id']
#         r_id = all_info["r_id"]
#         task = Task.query.filter(and_(Task.checker==checker_id, Task.r_id==r_id, Task.status=="checking")).first()
#         task.checked_info = all_info['checked_info']
#         task.status = "checked"
#         db.session.commit()
#         logger.info("%s_success|checker_id=%s", submit.__name__, checker_id)
#         return jsonify({"status": 1, "message": "submit successfully"}), 200
#     except Exception as e:
#         logger.error("%s_failed|input = %s|exception=%s", submit.__name__, e, exc_info=True)
#         return jsonify({'status': 0, 'message': "wrong input"}), 404
#
# manager = flask_restless.APIManager(view_bp,flask_sqlalchemy_db=db)
#
# manager.create_api(Task, methods=["GET"], url_prefix="/api/query")
#
# if __name__ == '__main__':
#     app.run()