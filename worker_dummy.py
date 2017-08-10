import time

import boto3
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


class Keys(object):
    user_agent = 'user_agent'
    msg_id = 'msg_id'
    queue_name = 'queue_name'
    receive_count = 'receive_count'
    my_secret = 'X-Aws-Sqsd-Attr-My-Secret'


parser = reqparse.RequestParser()
parser.add_argument('User-Agent', location='headers', dest=Keys.user_agent)
parser.add_argument('X-Aws-Sqsd-Msgid', location='headers', dest=Keys.msg_id)
parser.add_argument('X-Aws-Sqsd-Queue', location='headers', dest=Keys.queue_name)
parser.add_argument('X-Aws-Sqsd-Receive-Count', type=int, location='headers', dest=Keys.receive_count)
parser.add_argument(Keys.my_secret, location='headers', dest=Keys.my_secret)


class DynamoDbTable(object):
    def __init__(self, table_name):
        self._table_name = table_name
        self._table = boto3.resource('dynamodb').Table(self._table_name)

    def add_row(self):
        raise NotImplementedError()


class UsersTable(DynamoDbTable):
    def __init__(self):
        super(UsersTable, self).__init__('Users')

    def add_row(self, email_address, display_name, password):
        self._table.put_item(Item={
            'EmailAddress':email_address,
            'UserCreationTimeUtc':int(time.time()),
            'DisplayName':display_name,
            'Password':password,
        })


class Dummy(Resource):

    def __init__(self):
        self.table = UsersTable()

    def post(self):
        args = parser.parse_args()
        app.logger.info("msg id:        %s", args[Keys.msg_id])
        app.logger.info("queue name :   %s", args[Keys.queue_name])
        app.logger.info("recieve count: %s", args[Keys.receive_count])
        app.logger.info("my secret:     %s", args[Keys.my_secret])

        self.table.add_row(
            email_address=args[Keys.msg_id],
            display_name='placeholder',
            password=args[Keys.my_secret],
        )
        return '', 200

api.add_resource(Dummy, '/')

if __name__ == '__main__':
    app.run(debug=True)