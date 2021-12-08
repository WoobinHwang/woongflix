from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient

import random

app = Flask(__name__)

client = MongoClient('mongodb://test:test@52.79.33.194', 27017)
db = client.dbsparta

# client = MongoClient("localhost", 27017)
# db = client.dbMovie

movieList = db.tp7
comment = db.comment


app.secret_key = "ABCDEFG"


# main page view
@app.route("/")
def init():
    return render_template("index.html")


# register page view(회원가입)
@app.route("/register")
def register():
    return render_template("register.html")


# login page view(로그인)
@app.route("/login")
def login():
    return render_template("login.html")


# all movie list view
@app.route("/movies", methods=["GET"])
def movie_list():
    return render_template("movies.html")


# detail page view
@app.route("/detail", methods=["GET"])
def detail():
    return render_template("detail.html")


# 회원가입 진행(db에 저장)
@app.route("/sign_up", methods=["POST"])
def sign_up():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]

    doc = {"username": username_receive, "password": password_receive}
    db.users.insert_one(doc)

    return jsonify({"msg": "저장이 완료되었습니다"})


# id 중복 검사
@app.route("/sign_up/id_check", methods=["POST"])
def id_check():
    username_receive = request.form["username_give"]
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({"result": "success", "exists": exists})


# 로그인
@app.route("/sign_in", methods=["POST"])
def sign_in():

    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]

    print(username_receive, password_receive)

    result = db.users.find_one(
        {"username": username_receive, "password": password_receive}
    )

    if result is not None:
        session["username"] = result.get("username")

        return jsonify({"result": "success", "msg": "로그인 성공"})
    # 찾지 못하면
    else:
        return jsonify({"result": "fail", "msg": "아이디/비밀번호가 일치하지 않습니다."})


# 로그아웃
@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("init"))


@app.route("/comments", methods=["POST"])  # 해당 영화 조회를 하기위해 post로 바꿨습니다.
def get_comments():
    title_receive = request.form["title_give"]
    comments = list(
        db.comment.find({"title": title_receive}, {"_id": False})
    )  # title로 comment 조회
    return jsonify({"target_comments": comments})


# update comments
@app.route("/comments/update", methods=["POST"])
def update_comments():

    title_receive = request.form["title_give"]
    ID_receive = request.form["ID_give"]
    comment_receive = request.form["comment_give"]

    doc = {
        "title": title_receive,
        "ID": ID_receive,
        "comment": comment_receive,
    }  # title, id, comment로 저장
    db.comment.insert_one(doc)
    return jsonify({"msg": "등록 완료"})


# top 4 movie get 기분별 하나씩 랜덤하게 가져오기
@app.route("/recommend/top", methods=["GET"])
def get_recommend_top():
    recommend_top = []

    try:
        happy_list = list(movieList.find({"genre": "신남"}, {"_id": False}))
        today_happy = random.sample(happy_list, 1)[0]

        happy_title = today_happy["title"]
        happy_img = today_happy["img_url"]
        recommend_top.append(happy_title)
        recommend_top.append(happy_img)

        angry_list = list(movieList.find({"genre": "화남"}, {"_id": False}))
        today_angry = random.sample(angry_list, 1)[0]
        angry_title = today_angry["title"]
        angry_img = today_angry["img_url"]
        recommend_top.append(angry_title)
        recommend_top.append(angry_img)

        sad_list = list(movieList.find({"genre": "우울"}, {"_id": False}))
        today_sad = random.sample(sad_list, 1)[0]
        sad_title = today_sad["title"]
        sad_img = today_sad["img_url"]
        recommend_top.append(sad_title)
        recommend_top.append(sad_img)

        move_list = list(movieList.find({"genre": "떠남"}, {"_id": False}))
        today_move = random.sample(move_list, 1)[0]
        move_title = today_move["title"]
        move_img = today_move["img_url"]
        recommend_top.append(move_title)
        recommend_top.append(move_img)

    except Exception as e:
        print(recommend_top)
        return jsonify({"ERROR: fail to get top items"})

    return jsonify({"recommendTop": recommend_top})


# get all movie by genre
@app.route("/recommend/list", methods=["POST"])
def get_recommend_list():
    try:
        genre_receive = request.form["genre_name"]

        movie_list = list(
            movieList.find({"genre": genre_receive}, {"_id": False}).sort("score", -1)
        )

    except Exception:

        return jsonify({"error"})

    return jsonify({"movie_list": movie_list})


# get all genre movie list
@app.route("/find/all/score", methods=["GET"])
def find_all_movie_score():
    try:
        movie_list_all = list(movieList.find({}, {"_id": False}).sort("score", -1))

    except Exception:

        return jsonify({"error to find movies"})

    return jsonify({"movie_list": movie_list_all})


@app.route("/find/all/abc", methods=["GET"])
def find_all_movie_abc():
    try:
        movie_list_all = list(movieList.find({}, {"_id": False}).sort("title", 1))

    except Exception:

        return jsonify({"error to find movies"})

    return jsonify({"movie_list": movie_list_all})


# get movie detail
@app.route("/find", methods=["POST"])
def find_movie_detail():
    try:
        title_receive = request.form["title_give"]
        print(title_receive)

        target = movieList.find_one({"title": title_receive}, {"_id": False})
        print(target)

    except Exception as e:
        return {"message": "failed to search"}, 401

    return jsonify({"movie_data": target})


@app.route("/writeComment", methods=["POST"])
def write_comment():
    try:
        comment_receive = request.form["comment_give"]
        title_receive = request.form["title_give"]
        doc = {"comment": comment_receive}
        movieList.insert_one(
            movieList.find_one({{"title": title_receive}, {"_id": False}}).toArray(doc)
        )
    # db.B_COLLLECTION.insertMany(db.A_COLLLECTION.find({"reg_date": { $eq: '20190805'}}).toArray())

    except Exception as e:
        print("error", e)
        return {"message": "failed to search"}

    return jsonify({"msg": "comment delivery"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
