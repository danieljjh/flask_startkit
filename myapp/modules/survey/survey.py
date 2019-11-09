# -*- coding: UTF-8 -*-
"""
Api for Survey
"""

from flask import Blueprint, jsonify, request, current_app, abort, g
from myapp.model.models import *
import datetime as dt
from .xcx_lib import *
from .xls_fmt import *

app = current_app
blu_survey = Blueprint('survey', __name__, template_folder='../templates')
jyq_openid = "oFZqJ5Ya25bQlIGBNYlOBi0MWOoE"


@blu_survey.route('/xcx_login', methods=['GET'])
def xcx_login():
    """
        input：
            xcx 用户 wx.login  提交数据 code
        output：
            用户信息，用户是否已经回答问卷
    """
    code = request.args.get('code')
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': XCX_APPID,
        'secret': XCX_SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    r = requests.get(url, params=params).json()
    if 'openid' in r:
        xcxId = r['openid']
        wx_user = WxUser.find(xcxId=xcxId).one_or_none()
        if wx_user:
            user_info = row2dict(wx_user)
            user_id = user_info['id']
            user_quiz = SurveyResult.find(wx_user_id=user_id).all()
            if user_quiz:
                return jsonify(dict(status='done', userInfo=user_info))
            else:
                return jsonify(dict(status='user',  userInfo=user_info))
        else:
            new_wx_user = WxUser(xcxId=xcxId)
            db.session.add(new_wx_user)
            db.session.commit()
            return jsonify(dict(status='newuser',  userInfo=row2dict(new_wx_user), xcx_info=r))
    else:
        return jsonify(dict(status='error', userInfo={}))


@blu_survey.route('/survey_dtl', methods=['GET'])
def survey_dtl():
    survey_id = request.args.get('survey_id')
    survey_quiz = SurveyQuestions.find(survey_id=survey_id).all()
    res = [row2dict(x) for x in survey_quiz]
    return jsonify(res)


@blu_survey.route('/del_result', methods=['GET'])
def del_result():
    user_id = request.args.get('user_id')
    # survey_res = SurveyResult.find(wx_user_id=user_id).one_or_none()
    # if survey_res:
    #     result_id = row2dict(survey_res)['id']
    #     dtl = SurveyResultDtl.find(result_id=result_id)
    #     tt = dtl.all()
    #     [db.session.delete(x) for x in tt]
    #     db.session.delete(survey_res)
    #     db.session.commit()
    #     return jsonify(dict(status='success'))
    #     SurveyResultDtl.
    return jsonify(dict(data=''))


@blu_survey.route('/save_answer', methods=['POST'])
def save_answer():
    """
     my first api
     method: POST
     input:
            http://localhost:5000/api/my_post

            {
                "wx_user_id": 1,

                "answers": answers
            }
     output:
        json
    """
    data = request.get_json()
    user_id = data['wx_user_id']
    answers = data['answers']

    # check_survey = SurveyResult.find(
    # wx_user_id=user_id, survey_id=1).one_or_none()
    # if check_survey:
    #     return jsonify(dict(status='done'))
    # else:
    #: save and create new survey result for this user and survey and get id
    survey_result = SurveyResult(wx_user_id=user_id, survey_id=2)
    db.session.add(survey_result)
    db.session.commit()
    res_id = survey_result.id

    for x in answers:
        x.update(dict(result_id=res_id))
        del x['col_type']
        del x['values']
        sr = SurveyResultDtl(**x)
        db.session.add(sr)
        db.session.flush()
    db.session.commit()

    # res = dict(name=name, age=age, school=school)
    return jsonify(dict(status='success', res=res_id))


@blu_survey.route('/survey_statics', methods=['GET'])
def survey_statics():
    res = SurveyResult.query.all()
    return jsonify(dict(survey_count=len(res)))


@blu_survey.route('/dl_survey_result', methods=['GET', 'POST'])
def dl_survey_result():
    res = SurveyResultDtl.query.join(SurveyResult, SurveyResultDtl.result_id == SurveyResult.id).with_entities(
        SurveyResult.id.label('result_id'),
        SurveyResult.wx_user_id, SurveyResultDtl.question_id, SurveyResult.survey_id, SurveyResultDtl.label, SurveyResultDtl.value_type, SurveyResultDtl.value_cn
    ).all()
    data = [x._asdict() for x in res]
    return jsonify(data=data)


@blu_survey.route('/upload_content', methods=['GET', 'POST'])
def upload_content():
    '''
      upload learning content xls file
    '''
    if request.method == 'POST':
        # print request.form()
        f = request.files['file']
        table_name = request.form.get("table_name")

        df = pd.read_excel(f, sheet_name=0)
        res = save_xls_to_db(table_name, df)
        return jsonify(dict(content=survey_name, result=res))
    return render_template('upload_xls.html')


@blu_survey.route('/all_survey', methods=['GET'])
# ： 这个是 网址， methods: 指定这个网址可以接受 哪种 request
# route 是 外部调用的 地址 ， 而 def 的名称是 用于内部 function 调用的
def survey_list():
    """
     list survey
     method: GET
     input:
            http://localhost:5000/survey/survey_list
     output:
        json
    """
    surveys = Surveys.find(active=True).all()
    res = [row2dict(x) for x in surveys]
    # 用 jsonify 把 dict 转为 json
    return jsonify(res)
