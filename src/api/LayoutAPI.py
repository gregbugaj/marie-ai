from flask_restful import Resource, reqparse


class LayoutListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(LayoutListAPI, self).__init__()

    def get(self):
        return {}, 200

    def post(self):
        pass

class LayoutAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(LayoutAPI, self).__init__()    

    def get(self, id):
        return {'qeueue_id':id}, 200

    def put(self, id):
        pass

    def delete(self, id):
        pass
       