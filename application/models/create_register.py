from models import User
from .database import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import decode_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError, InvalidSignatureError
import re
from flask import abort, jsonify, flash
from .crud import CRUD

class CreateRegister(CRUD):

    def user_register(self, password, email):

        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(user=email, password=hashed_password)
        ## CRUD継承・DB登録
        result = self.db_insert(new_user)
        if result == False:
            abort(500, 'ユーザー登録できませんでした')
        return jsonify({ 'message': 'ユーザー登録しました', 'code': 200 })
    
    ## 有効なトークンか確認
    def validation_token(self, input_token):
        try:
            token = decode_token(input_token)
        
        except ExpiredSignatureError:
            abort(401, 'トークンの有効期限が切れています')
            
        except (DecodeError, InvalidTokenError, InvalidSignatureError):
            abort(400, '不正なトークンです')
        
        except Exception:
            abort(500, 'トークンが正常に読み込まれませんでした')

        else:
            return token

    def reset_password(self, password, email):

        reset_user = User.query.filter_by(user=email).first()

        if reset_user == None:
            flash('パスワードの変更に失敗しました')
            return False
        
        reset_user.password = generate_password_hash(password, method='scrypt')
        db.session.commit()
        flash('パスワードを変更しました')
        return True