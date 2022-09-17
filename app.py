from flask import Flask,render_template,request,jsonify,make_response
import pandas as pd
import student
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_mongoengine import MongoEngine




app = Flask(__name__)

database_name = "Quiz-app"
DB_URI = "mongodb+srv://researchUser:dbUserPassword@quiz-app.bebjkg9.mongodb.net/?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

# @app.route('/predict',methods=['POST','GET',])
# def index():
#     if  request.method == 'POST':
#         user_input = request.form.get('marks')
#         print(user_input)
#         prediction=student.performance_predict(user_input)
#         print(prediction)
#     return render_template('home.html')

# @app.route("/predict",methods=["POST"])
# def predict():
#     json_ = request.json
#     prediction = rnn.performance_predict(json_)
#     return jsonify({"Prediction" : list(prediction)})

class Question(db.Document):
    question_id = db.SequenceField()
    question = db.StringField()
    answer = db.StringField()
    option1 = db.StringField()
    option2 = db.StringField()
    option3 = db.StringField()
    option4 = db.StringField()
    subject = db.StringField()
    section = db.StringField()
    difficulty = db.StringField()

    def to_json(self):
        return {
            "question_id":self.question_id,
            "question":self.question,
            "answer":self.answer,
            "option1":self.option1,
            "option2":self.option2,
            "option3":self.option3,
            "option4":self.option4,
            "subject":self.subject,
            "section":self.section,
            "difficulty":self.difficulty
        }

class QuestionAnswers(db.EmbeddedDocument):
    question_id = db.IntField()
    response = db.StringField()

class UserResponse(db.Document):
    response_id = db.SequenceField()
    quiz_id = db.IntField()
    quiz_answers = db.EmbeddedDocumentListField(QuestionAnswers)
    score = db.IntField()

    def to_json(self):
        return {
            "quiz_id":self.quiz_id,
            "quiz_answers":self.quiz_answers,
            "score":self.score
        }

# class Quiz(db.Document):
#     quiz_id = db.SequenceField()
#     quiz_name = db.StringField()
#     question_id = db.ListField()



#     def to_json(self):
#         return {
#             "quiz_id":self.quiz_id,
#             "quiz_name":self.quiz_name,
#             "question_id":self.question_id
#         }

class Quiz(db.Document):
    quiz_id = db.SequenceField()
    quiz_name = db.StringField()
    question_1 = db.IntField()
    question_2 = db.IntField()
    question_3 = db.IntField()
    question_4 = db.IntField()
    question_5 = db.IntField()
    section = db.StringField()
    score = db.IntField()




    def to_json(self):
        return {
            "quiz_id":self.quiz_id,
            "quiz_name":self.quiz_name,
            "question_1":self.question_1,
            "question_2":self.question_2,
            "question_3":self.question_3,
            "question_4":self.question_4,
            "question_5":self.question_5,
            "section":self.section,
            "score":self.score
        }



    @app.route('/api/db_populate', methods=['POST'])
    def db_populate():
        question1 = Question(question_id = 1,question = "If y= cosx, then what is the maximum value of y?",answer = "1",option1 = "1",option2 = "-1",option3 = "3.14",option4 = "6.28",subject = "mathematics",section = "trignonmetry",difficulty = "")
        question1.save()
        return make_response("",201)


    @app.route('/api/questions', methods=['GET','POST'])
    def api_questions():
        if request.method == 'GET':
            questions = []
            for question in Question.objects:
                questions.append(question)
            return make_response(jsonify(questions),200)
        elif request.method == 'POST':
            content = request.json
            question = Question(question = content["question"],answer = content["answer"],option1 = content["option1"],option2 = content["option2"],option3 = content["option3"],option4 = content["option4"],subject = content["subject"],section = content["section"],difficulty = content["difficulty"])
            question.save()
            return make_response(jsonify(question),200)

    @app.route('/api/questions/<question_id>', methods=['GET','PUT','DELETE'])
    def api_each_question(question_id):
        if request.method =='GET':
            question_obj = Question.objects(question_id=question_id).first()
            if question_obj:
                return make_response(jsonify(question_obj.to_json()),200)
            else:
                return make_response("Not found",404)

        elif request.method =='PUT':
            content = request.json
            question_obj = Question.objects(question_id=question_id).first()
            question_obj.update(question = content["question"],answer = content["answer"],option1 = content["option1"],option2 = content["option2"],option3 = content["option3"],option4 = content["option4"],subject = content["subject"],section = content["section"],difficulty = content["difficulty"])
            return make_response(jsonify(question_obj.to_json()),204)
            
        elif request.method =='DELETE':
            question_obj = Question.objects(question_id=question_id).first()
            question_obj.delete()
            return make_response("question deleted",200)


    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions',None)
        section = body.get('section',None)

        try:
            questionAll = Question.query.filter(
                Question.section == section).all()
            questions = [question.format() for question in questionAll]
            if questions == []:
                abort(404)

            quiz = [i for i in previous_questions if i not in questions] + [j for j in questions if j not in previous_questions]

            return jsonify({
                'success':True,
                'questions':[quiz],
            })

        except Exception:
            abort(400)

        
        
    @app.route('/api/sections/<section>', methods=['GET'])
    def api_each_section(section):
        if request.method == 'GET':
            questions = []
            for question in Question.objects(section=section):
                questions.append(question)
            return make_response(jsonify(questions),200)

    @app.route('/api/result/<quiz_id>', methods=['GET'])
    def api_section_result(quiz_id):
        if request.method == 'GET':
            results = []
            for result in UserResponse.objects(quiz_id=quiz_id):
                results.append(result)
            return make_response(jsonify(results),200)

    # @app.route('/api/quiz', methods=['POST'])
    # def attempt_quiz():
    #         total_marks = 0
    #         for i in request.json['quiz_answers']:
    #             c = UserResponses(quiz_id=request.json['quiz_id'], user_id=user_id, question_id=i['question_id'], response=i['answer'], is_active=1)
    #             db.session.add(c)
    #             if Questions.objects(question_id=i['question_id']).first().answer == i['answer']:
    #                 total_marks += QuestionMaster.query.filter_by(question_id=i['question_id']).first().marks
    #         li.score_achieved = total_marks
    #         li.is_submitted = 1
    #         db.session.commit()
    #         return {"total_marks": total_marks, "message":"Quiz Submitted Successfully"}

    @app.route('/api/quiz', methods=['POST'])
    def api_quiz():
        content = request.json
        questions = []
        quiz = Quiz(quiz_name = content["quiz_name"],question_1 = content["question_1"],question_2 = content["question_2"],question_3 = content["question_3"],question_4 = content["question_4"],question_5 = content["question_5"],section = content["section"])
   
        # m = Question.objects(question_id=int(content["question_id"])).first()
        # questions.append(m)
        quiz.save()
        return make_response(jsonify(quiz),200)
        

    # @app.route('/api/quiz/<quiz_id>', methods=['GET'])
    # def api_viewquiz(quiz_id):
    #     quiz = Quiz.objects(quiz_id=quiz_id)
    #     if quiz:
    #         return make_response(jsonify(quiz.to_json()),200)
    #     else:
    #         return make_response("Not found",404)

    # @app.route('/api/quiz/<quiz_id>', methods=['GET'])
    # def api_viewquiz(quiz_id):
    #     if request.method == 'GET':
    #         quizzes = []
    #         for quiz in Quiz.objects(quiz_id=quiz_id):
    #             quizzes.append(quiz)
    #         return make_response(jsonify(quizzes),200)

    # @app.route('/api/quiz/<quiz_id>', methods=['GET'])
    # def api_viewquiz(quiz_id):
    #     quiz_name = Quiz.objects(quiz_id=quiz_id).first().quiz_name
    #     li_1 = Quiz.objects(quiz_id=quiz_id)
    #     li_2 = []
    #     for i in li_1:
    #         li_2.append(i.question_id)
    #     params = []
    #     for j in li_2:
    #         m = Question.objects(question_id=j).first() 
    #     return make_response(jsonify(m),200)

        #     question_info = {"question_id":m.question_id, "question":m.question,"answer":m.answer, "option1":m.option1, "option2":m.option2, "option3":m.option3, "option4":m.option4,}
        #     params.append(question_info) 
        # return {"quiz_id":quiz_id,"Quiz Name":quiz_name, "Quiz Questions":params}, 200
        

    @app.route('/api/quiz/<quiz_id>', methods=['GET'])
    def api_viewquiz(quiz_id):
            quiz_name = Quiz.objects.get(quiz_id=quiz_id).quiz_name
            li_1 = Quiz.objects(quiz_id=quiz_id)
            li_2 = []
            for i in li_1:
                li_2.append(i.question_1)
                li_2.append(i.question_2)
                li_2.append(i.question_3)
                li_2.append(i.question_4)
                li_2.append(i.question_5)
            params = []
            for j in li_2:
                m = Question.objects(question_id=j).first()
                question_info = {"question_id":m.question_id, "question":m.question,"answer":m.answer, "option1":m.option1, "option2":m.option2, "option3":m.option3, "option4":m.option4}
                params.append(question_info)
            return {"quiz_id":quiz_id, "Quiz_Name":quiz_name, "Quiz_Questions":params}, 200
                
            #     params.append(question_info) 
            # return {"quiz_id":request.json['quiz_id'], "Quiz Name":quiz_name, "Quiz Questions":params}, 200

    @app.route('/api/attempt/<quiz_id>', methods=['POST','PUT'])
    def api_attempt_quiz(quiz_id):
        answer_arr = []

        total_marks = 0
        content = request.json
        for i in content['quiz_answers']:
            req = request.json
            answer_arr.append(i)
            q=Question.objects.get(question_id=i["question_id"])
            if q.answer == i['response']:
                total_marks += 10  
        m = UserResponse(quiz_id = quiz_id,quiz_answers=answer_arr,score=total_marks)
        m.save()
        return make_response(jsonify(m),200)

        # return {"total_marks":total_marks, "message":"Quiz Submitted Successfully"}, 200


 



    # @app.route('/api/quiz', methods=['GET','POST'])
    # def api_quiz():
    #     request.method == 'GET':
    #     questions = []
    #     for question in Question.objects:
    #         questions.append(question)
    #     return make_response(jsonify(questions),200)
    #     elif request.method == 'POST':
    #         quiz = Quiz(question_name = content["question_name"],question_id = content["question_id"])
    #         quiz.save()
    #         return make_response(jsonify(quiz),200)

    # @app.route('/api/sections', methods=['GET'])
    # def api_all_section():
    #     if request.method == 'GET':
    #         sections = []
    #         for section in Question.section:
    #             sections.append(section)
    #         return make_response(jsonify(sections),200)
        


if __name__ == "__main__":
    app.run(debug=True)