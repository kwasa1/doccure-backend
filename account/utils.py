from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail, send_mass_mail, EmailMessage
from smtplib import SMTPException


class ActivationMailFormMixin:
    mail_validation_error = ""
    # check if form was sent
    @property
    def mail_sent(self):
        if hasattr(self, "_mail_sent"):
            return self._mail_sent
        
        return False
    # ensure no manipulation of the 
    # mail_sent property
    @mail_sent.setter
    def set_mail_sent(self):
        raise TypeError("Cannot set mail_sent attribute")
    
    def get_message(self, *args, **kwargs):
        # obtain the template name from the view, 
        # in this case the name must be the same as 
        # what is in the kwargs get
        email_template_name = kwargs.get("email_template_name")
        context = kwargs.get("context")
        # site_context = kwargs.get("site_context")
        
        return render_to_string(email_template_name, context)
    
    # user the same technique in the above to getb subject
    def get_subject(self, *args, **kwargs):
        subject_template_name = kwargs.get("subject_template_name")
        context = kwargs.get("context")
        subject = render_to_string(subject_template_name, context)
        
        subject = "".join(subject.splitlines())
        return subject
    # now build the actual context
    # if not set we build 
    
    def get_context_data(self, request, user, context=None):
        # assertain if context not set then create
        if context is None:
            context = {}
            current_site = get_current_site(request)
            if request.is_secure() or not settings.DEBUG:
                protocol = "https"
            else:
                protocol = "http"
            token = token_generator.make_token(user)
            uid= urlsafe_base64_encode(force_bytes(user.pk))
            context.update({
                "domain":current_site.domain,
                "protocol":protocol,
                "site_name":current_site.name,
                "token":token,
                "uid":uid,
                "user":user
            })
        return context
    
    # sndinf email
    def _send_mail(self, request, user, *args, **kwargs):
        kwargs['context'] = self.get_context_data(request, user)
        mail_kwargs = {
            "subject":self.get_subject(**kwargs),
            "message":self.get_message(**kwargs),
            "from":(
                settings.DEFAULT_FROM_EMAIL
            ),
            "recipients":[user.email, ]
        }
        # try except to cathc any erros
        
        try:
            number_sent= send_mail(**kwargs)

        except Exception as e:
            self.log_mail_error(error=e, **mail_kwargs)
            if isinstance(e, BadHeaderError):
                err_code = "BadHeaderError"
            elif isinstance(e, SMTPException):
                err_code = "SMTPException Error"
        else:
            err_code = "EnexpectedError"
            if number_sent > 0:
                return (True, None)
        self.log_mail_error(**mail_kwargs)
        return (False, err_code)
    