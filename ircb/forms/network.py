from wtforms_alchemy import ModelForm
from wtforms.fields import SelectField

from ircb.models import Network
from ircb.models.network import SSL_VERIFY_CHOICES


class NetworkForm(ModelForm):
    class Meta:
        model = Network
        exclude = [
            'status',
            'rhost',
            'rport',
            'lhost',
            'lport',
            'access_token',
            'current_nickname'
        ]

    ssl_verify = SelectField(default='CERT_NONE', choices=SSL_VERIFY_CHOICES)
