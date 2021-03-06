from django.contrib.staticfiles.storage import staticfiles_storage
from shark.base import Object, StringParam


class ProfilePanel(Object):
    def __init__(self, name='', profile_pic='', background_pic='', description='', **kwargs):
        self.init(kwargs)

        self.name = self.param(name, StringParam, 'Name of the person')
        self.profile_pic = self.param(profile_pic, StringParam, 'URL to the picture of the person')
        self.background_pic = self.param(background_pic, StringParam, 'URL to a background picture')
        self.description = self.param(description, StringParam, 'Description of the person')

    def get_html(self, html):
        html.append('<div class="panel panel-default panel-profile">')
        html.append('    <div class="panel-heading" style="background-image: url({});">'.format(self.background_pic))
        html.append('    </div>')
        html.append('    <div class="panel-body text-center">')
        html.append('        <img class="panel-profile-img" src="{}">'.format(self.profile_pic))
        html.append('        <h5 class="panel-title">{}</h5>'.format(self.name))
        html.append('        <p class="m-b">{}</p>'.format(self.description))
        html.append('    </div>')
        html.append('</div>')

        html.add_resource(staticfiles_storage.url('shark/css/profile.css'), 'css', 'themes', 'profile')
