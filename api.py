from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
from make_tex import make_tex

app = Flask(__name__)
api = Api(app)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

guide_model = api.model(name='Guide Details',
                        model={
                            'name':
                            fields.String('Guide Name', required=True),
                            'designation':
                            fields.String('Guide Designation', required=True),
                            'department':
                            fields.String('Guide Department', required=True),
                        })

hod_model = api.model(name='HOD Details',
                      model={
                          'name':
                          fields.String('Guide Name', required=True),
                          'department':
                          fields.String('Guide Department', required=True),
                      })

author_model = api.model(name='Author Details',
                         model={
                             'name':
                             fields.String('Author Name', required=True),
                             'regno':
                             fields.String('Author Registration Number',
                                           required=True)
                         })

metadata_model = api.model(name='Metadata',
                           model={
                               'title':
                               fields.String('Project Title', required=True),
                               'guide':
                               fields.Nested(guide_model, required=True),
                               'hod':
                               fields.Nested(hod_model, required=True),
                               'author':
                               fields.List(fields.Nested(author_model),
                                           required=True),
                               'biblio-files':
                               fields.String('Bibliography File',
                                             required=True),
                               'submission-date':
                               fields.String('Submission Date', required=True),
                               'abstract':
                               fields.String('Abstract', required=True)
                           })

data_model = api.model(name='Data', model={
    'markdown_text': fields.String('Markdown text', required=True),
    'metadata': fields.Nested(metadata_model, required=True),
})


@api.route("/make-tex")
class Dehaze(Resource):

    @api.expect(data_model)
    def post(self):

        try:
            metadata = api.payload['metadata']
            markdown_text = api.payload['markdown_text']

            latex_text = make_tex(metadata_dict=metadata,
                                  markdown_text=markdown_text)

            return {'success': True, 'latex_text': latex_text}, 200

        except Exception as e:
            print(e)
            return {'success': False}, 422


if __name__ == "__main__":
    app.run(debug=True)
