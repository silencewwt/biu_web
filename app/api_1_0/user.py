# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app

from app import db
from app.models import User, Fan
from app.utils.image import upload_image
from . import api
from api_constants import *


@api.route('/register')
def register():
    data = {'user': {}}
    password = request.values.get('password', '', type=str)
    identity = request.values.get('identity', '', type=str)
    mobile = request.values.get('mobile', '', type=str)
    user = User.query.filter_by(mobile=mobile).limit(1).first()
    if user:
        data['status'] = MOBILE_EXIST
        data['message'] = MOBILE_EXIST_MSG
    elif mobile and password and identity:
        user = User(
            id=User.get_random_id(),
            nickname='',
            password=password,
            mobile=mobile,
            identity=identity,
        )
        db.session.add(user)
        db.session.commit()
        data['user'] = user.get_self_info_dict()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/login')
def login():
    data = {'user': {}}
    mobile = request.values.get('mobile', '', type=str)
    password = request.values.get('password', '', type=str)
    identity = request.values.get('identity', '', type=str)
    user = User.query.filter_by(mobile=mobile).limit(1).first()
    if user and user.verify_password(password):
        user.update_identity(identity)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
        data['user'] = user.get_self_info_dict()
    else:
        data['status'] = LOGIN_FAIL
        data['message'] = LOGIN_FAIL_MSG
    return jsonify(data)


@api.route('/profile')
def profile():
    data = {'profile': {}}
    user_id = request.values.get('user_id', '', type=str)
    page = request.values.get('page', 1, type=int)
    user = User.query.get(user_id)
    if user:
        data['profile'] = user.get_profile_dict(page)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    return jsonify(data)


@api.route('/push_setting')
def push_setting():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    push = request.values.get('push', SETTING_IS_NOT_VALID, type=int)
    disturb = request.values.get('disturb', SETTING_IS_NOT_VALID, type=int)
    user = User.query.get(user_id)
    print(push, disturb)
    if not user:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    else:
        if push > SETTING_IS_NOT_VALID:
            user.push = push
        if disturb > SETTING_IS_NOT_VALID:
            user.disturb = disturb
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    return jsonify(data)


@api.route('/personal_info_setting')
def personal_info_setting():
    data = {}
    image_str = request.values.get('image_str', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    nickname = request.values.get('nickname', u'', type=unicode)
    signature = request.values.get('signature', u'', type=unicode)
    user = User.query.get(user_id)
    if user:
        if image_str:
            avatar_path = upload_image(user.id, image_str)
            if avatar_path:
                user.avatar = avatar_path
            else:
                data['status'] = NOT_IMAGE
                data['message'] = NOT_IMAGE_MSG
                return jsonify(data)
        user.nickname = nickname
        user.signature = signature
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    return jsonify(data)


@api.route('/follow')
def follow():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    idol_id = request.values.get('idol_id', '', type=str)
    cancel = request.values.get('cancel', 0, type=int)
    user = User.query.get(user_id)
    idol = User.query.get(idol_id)
    if user and idol:
        fan = Fan.query.filter_by(user_id=user_id, idol_id=idol_id).limit(1).first()
        if not fan and not cancel:
            fan = Fan(user_id=user_id, idol_id=idol_id)
            db.session.add(fan)
            db.session.commit()
            # TODO: 关注推送
        elif fan.is_deleted and not cancel:
            fan.is_deleted = False
        elif fan and cancel:
            fan.is_deleted = True
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/follow_list')
def follow_list():
    data = {'follows': []}
    user_id = request.values.get('user_id', '', type=str)
    page = request.values.get('page', 1, type=int)
    following = request.values.get('following', 1, type=int)
    target_id = request.values.get('target_id', '', type=str)
    user = User.query.get(user_id)
    target = User.query.get(target_id)
    if target:
        follows = target.get_fans(following, page, current_app.config['FOLLOW_LIST_PER_PAGE'])
    elif user:
        follows = user.get_fans(following, page, current_app.config['FOLLOW_LIST_PER_PAGE'])
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
        return jsonify(data)
    for follow_ in follows:
        fan = Fan.query.filter_by(user_id=user_id, idol_id=follow_.idol_id, is_deleted=False).limit(1).first()
        followed = True if fan else False
        follow_dict = follow_.get_user_or_idol(following).get_brief_info_dict()
        follow_dict['followed'] = followed
        data['follows'].append(follow_dict)
    data['status'] = SUCCESS
    data['message'] = SUCCESS_MSG
    return jsonify(data)