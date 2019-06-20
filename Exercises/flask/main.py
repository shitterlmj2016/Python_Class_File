import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

emr_db = {
    'patients': {
        "p001": {'exams': {"e001": {"images": {"i001": "001.jpg", "i002": "002.jpg"}}}},
        "p002": {'exams': {"e002": {"images": {"i003": "003.jpg", "i004": "004.jpg"}}}},
        "p003": {'exams': {"e003": {"images": {"i005": "005.jpg", "i006": "006.jpg"}}}}}
}


class ElectronicMedicalRecord(Resource):
    def get(self):
        return emr_db


class PatientList(Resource):
    def get(self):
        return list(emr_db['patients'].keys())

    def post(self):
        data = json.loads(request.data)
        num_patients = len(emr_db['patients'].keys())
        patient_id = "p{0:0>3}".format(num_patients + 1)
        emr_db['patients'][patient_id] = data
        return emr_db['patients'][patient_id], 201


class Patient(Resource):
    def get(self, patient_id):
        return emr_db['patients'][patient_id]


class ExamList(Resource):
    def get(self, patient_id):
        return list(emr_db['patients'][patient_id]['exams'].keys())


class Exam(Resource):
    def get(self, patient_id, exam_id):
        return emr_db['patients'][patient_id]['exams'][exam_id]


class ImageList(Resource):
    def get(self, patient_id, exam_id):
        return list(emr_db['patients'][patient_id]['exams'][exam_id]['images'].keys())

    def post(self, patient_id, exam_id):
        data = json.loads(request.data)
        
        num_images = len(emr_db['patients'][patient_id]['exams'][exam_id]['images'].keys())
        image_id = "i{0:0>3}".format(num_images + 1)
        emr_db['patients'][patient_id]['exams'][exam_id]['images'][image_id] = data

        return emr_db['patients'][patient_id]['exams'][exam_id]['images'][image_id], 201


class Image(Resource):
    def get(self, patient_id, exam_id, image_id):
        return emr_db['patients'][patient_id]['exams'][exam_id]['images'][image_id]

    def put(self, patient_id, exam_id, image_id):
        data = json.loads(request.data)
        emr_db['patients'][patient_id]['exams'][exam_id]['images'][image_id] = data

        return emr_db['patients'][patient_id]['exams'][exam_id]['images'][image_id]

    def delete(self, patient_id, exam_id, image_id):
        del emr_db['patients'][patient_id]['exams'][exam_id]['images'][image_id]
        return '', 204

api.add_resource(ElectronicMedicalRecord, '/')
api.add_resource(PatientList, '/patients')
api.add_resource(Patient, '/patients/<patient_id>')
api.add_resource(ExamList, '/patients/<patient_id>/exams')
api.add_resource(Exam, '/patients/<patient_id>/exams/<exam_id>')
api.add_resource(ImageList, '/patients/<patient_id>/exams/<exam_id>/images')
api.add_resource(Image, '/patients/<patient_id>/exams/<exam_id>/images/<image_id>')


if __name__ == '__main__':
    app.run(debug=True)
