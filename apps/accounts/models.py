from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
# from imagekit.models import ProcessedImageField
from .managers import EmailUserManager
from .permissions import BaseUserPermission
import uuid


class EmailUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """

    FOOD_TYPE = (
        ('V', 'Veg'),
        ('N', 'Non-veg'),
    )

    TIMMING = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
    )

    PAY = (
        ('M', 'Monthly'),
        ('W', 'Weekly'),
        ('O', 'Ontime'),
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    tiffin_provider_name = models.CharField(_('Tifin Name'),
                                            max_length=300,
                                            blank=True)

    is_seller = models.BooleanField(_('is seller'), default=False)
    is_buyer = models.BooleanField(_('is buyer'), default=False)
    phone_number = models.CharField(_('Phone Number'),
                                    max_length=15,
                                    blank=True,
                                    null=True)
    birth_date = models.DateField(_("Date"), blank=True, null=True)
    is_notification_sound = models.BooleanField(default=True)
    is_notification_vibrate = models.BooleanField(default=True)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # validated_at = models.DateTimeField(null=True, blank=True)
    # validation_key = models.UUIDField(default=uuid.uuid4,
    #                                   null=True,
    #                                   blank=True)
    # is_terms_conditions_accepted = models.BooleanField(default=False)
    # terms_conditions = models.ForeignKey('contacts.TermsConditions',
    #                                      models.PROTECT,
    #                                      blank=True,
    #                                      null=True)
    # timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_seller_approved = models.BooleanField(default=False)
    is_social = models.BooleanField(default=False)
    food_type = models.CharField(max_length=1, choices=FOOD_TYPE)
    pay = models.CharField(max_length=1, choices=PAY)

    #Provider Details
    # provider_logo = ProcessedImageField(upload_to='CompanyLogo/',
    #                                     processors=[ResizeToFill(250, 250)],
    #                                     format='JPEG',
    #                                     options={'quality': 60},
    #                                     blank=True,
    #                                     null=True)
    # background_image = ProcessedImageField(upload_to='BackgroundImages/',
    #                                        processors=[ResizeToFill(550, 550)],
    #                                        format='JPEG',
    #                                        options={'quality': 60},
    #                                        blank=True,
    #                                        null=True)

    # Account Validation
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # validated_at = models.DateTimeField(null=True, blank=True)
    # validation_key = models.UUIDField(default=uuid.uuid4,
    #                                   null=True,
    #                                   blank=True)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def _send_html_mail(self, subject, template_html, template_text,
                        **context):
        """
        Renders templates to context, and uses EmailMultiAlternatives to
        send email.
        """
        if not template_html:
            raise ValueError('No HTML template provided for email.')
        if not template_text:
            raise ValueError('No text template provided for email.')
        default_context = {"settings": settings, "user": self}
        default_context.update(context)
        from_email = settings.DEFAULT_FROM_EMAIL
        body_text = render_to_string(template_text, default_context)
        body_html = render_to_string(template_html, default_context)

        msg = EmailMultiAlternatives(subject=subject,
                                     body=body_text,
                                     from_email=from_email,
                                     to=[self.email])
        msg.attach_alternative(body_html, 'text/html')
        msg.send()

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    # Set the user as active
    def validate(self) -> None:
        """
        Marks a user as validated and sends a confirmation email, clearing the
        validation_key so the validation link only works once.
        """
        # self.validation_key = None
        print('########################################################')
        print(self)
        self.validation_key = uuid.uuid4()
        self.validated_at = datetime.now()
        self.save()
        self._send_html_mail('Your account has been validated',
                             'email/user_validated.html',
                             'email/user_validated.txt')

    def send_validation_email(self):
        """
        Send email with a unique link using validation_key to validate account.
        """
        if self.is_social == False:
            self.validation_key = uuid.uuid4()
            self.save()
            self._send_html_mail(
                'Please validate your email address',
                'email/user_validation.html',
                'email/user_validation.txt',
                url='http://' + settings.SITE_DOMAIN +
                reverse('user-validation',
                        kwargs={"validation_key": self.validation_key}))

    def send_reset_password_email(self, request):
        """
        Send email with unique link to reset password. Create a new
        validation_key, which will be cleared once password is reset.
        """
        self.validation_key = uuid.uuid4()
        self.save()
        self._send_html_mail(
            'Password Reset Request',
            'email/user_reset_password.html',
            'email/user_reset_password.txt',
            url='http://' + settings.SITE_DOMAIN +
            reverse('reset-request',
                    kwargs={"validation_key": self.validation_key}))

    def send_reset_password_success_email(self):
        """
        Send email notifying users that their password was successfully reset.
        Validation key is cleared so the reset password link only works once.
        """
        self.validation_key = None
        self.save()
        self._send_html_mail('Password successfully changed',
                             'email/user_reset_password_success.html',
                             'email/user_reset_password_success.txt')
