from django.conf import settings
from django.views import generic
from django.utils.translation import gettext_lazy as _
from .forms import RegistrationForm
from django.urls import reverse_lazy
from .models import Account, RazorpayTransaction
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from . import razorpay
from .exceptions import UnableToTakePayment
from django.contrib import messages
# from django.core.mail import send_mail
from django.apps import apps
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .utils import EmailThread
# Create your views here.

# BannerImages = apps.get_model('registration', 'BannerImages')

#
# class Index(generic.TemplateView):
#     template_name = 'registration/index.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(Index, self).get_context_data(*args, **kwargs)
#         context['banner_images'] = BannerImages.objects.all()
#         return context


class Register(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('registration:payment')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        self.object = form.save()
        self.request.session['tnx_id'] = self.object.id
        return HttpResponseRedirect(self.get_success_url())


class PaymentView(generic.TemplateView):
    template_name = 'registration/payment.html'

    def get(self, request, *args, **kwargs):
        if 'tnx_id' not in request.session:
            raise Http404
        context = super(PaymentView, self).get(request, *args, **kwargs)
        return context

    def get_context_data(self, *args, **kwargs):
        rg_id = self.request.session['tnx_id']
        del self.request.session['tnx_id']
        account_model_instance = get_object_or_404(Account, id=rg_id)
        kwargs = super(PaymentView, self).get_context_data(*args, **kwargs)
        kwargs = {
            "amount": int(account_model_instance.amount) * 100,
            "rz_key": settings.RAZORPAY_API_KEY,
            "email": account_model_instance.email,
            "phonenumber": account_model_instance.phonenumber,
            "reg_id": rg_id,
            "txn_id": account_model_instance.txn_id,
            "name": account_model_instance.name,
            "phone": account_model_instance.phonenumber,
            "description": "Registration",
            "theme_color": getattr(
                settings, "RAZORPAY_THEME_COLOR", "#019d57"
            ),
            "logo_url": getattr(
                settings, "RAZORPAY_VENDOR_LOGO",
                "/static/images/logo.png"),
        }
        return kwargs


class PaymentSucessView(generic.RedirectView):

    permanent = False

    def get(self, request, *args, **kwargs):
        try:

            self.razorpay_id = request.GET['razorpay_id']
            self.transaction_id = request.GET['transaction_id']
            if not self.check_payment_captured(self.razorpay_id, self.transaction_id):
                messages.error(request, "Payment already Captured")
                return HttpResponseRedirect(reverse_lazy('registration:thank-you'))

        except Exception as e:
            print(str(e))
            raise Http404
        try:
            self.transaction_status = razorpay.update_transaction_details(
                self.razorpay_id, self.transaction_id)
        except Exception as e:
            messages.error(request, "Transaction Failed {0}".format(str(e)))
            return HttpResponseRedirect(reverse_lazy('registration:register'))
        try:
            confirm_txn = razorpay.capture_transaction(
                request, self.razorpay_id)
            # razorpay.initiate_bank_transfer(request, self.razorpay_id)
        except Exception:
            raise UnableToTakePayment()
        if not confirm_txn.is_successful:
            messages.error(self.request, _("""Razorpay Transaction Failed
                                              due to insufficent amount"""))
            raise UnableToTakePayment()
        else:
            account_model_instance = get_object_or_404(
                Account, txn_id=self.transaction_id)
            account_model_instance.payment_status = 'captured'
            account_model_instance.razp_id = self.razorpay_id
            account_model_instance.save()
            email_admin_body = render_to_string(
                                    "emailer/admin_emailer.html",
                                    {"account": account_model_instance})
            self.send_email(email_admin_body, account_model_instance,
                            settings.KIMS_CC_EMAIL,
                            settings.KIMS_ADMIN_EMAIL)
            email_user_body = render_to_string(
                                    "emailer/user_emailer.html",
                                    {"account": account_model_instance})
            self.send_email(email_user_body, account_model_instance,
                            to=account_model_instance.email)
        return super(PaymentSucessView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse_lazy('registration:thank-you')

    def check_payment_captured(self, rz_id, tnx_id):
        payment_dtails = Account.objects.get(txn_id=tnx_id)
        if payment_dtails.payment_status == "captured":
            return False
        return True

    def send_email(self, email_html_body,
                   account_model_instance, cc=None, to=None):
        EmailThread(email_html_body, 'dheeraj@webenza.com', to, cc).start()
        # email_object = EmailMultiAlternatives(subject='KIMS-CSR Donation',
        #                                       from_email=settings.FROM_EMAIL,
        #                                       to=[to],
        #                                       cc=cc)
        # email_object.attach_alternative(email_html_body, "text/html")
        # email_object.send()


class ThankYouView(generic.TemplateView):
    template_name = "registration/thank-you.html"


class CancelResponseView(generic.RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        account_model_instance = get_object_or_404(Account,
                                                    id=kwargs['rg_id'])
        account_model_instance = self.update_account_model(
            account_model_instance)
        razorpay_transaction_instance = get_object_or_404(RazorpayTransaction,
                                                          transaction_id=kwargs['tnx_id'])
        razorpay_transaction_instance = self.update_transaction_details(
            razorpay_transaction_instance)

        return super(CancelResponseView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, _("Razorpay transaction cancelled"))
        return reverse_lazy('registration:register')

    def update_account_model(self, account_model_instance):
        account_model_instance.payment_status = "Cancelled by user"
        account_model_instance.save()
        return account_model_instance

    def update_transaction_details(self, razorpay_transaction_instance):
        razorpay_transaction_instance.status = 'Cancelled by user'
        razorpay_transaction_instance.save()
        return razorpay_transaction_instance


class TermsView(generic.TemplateView):
    template_name = "registration/terms.html"


class PrivacyView(generic.TemplateView):
    template_name = "registration/privacy.html"


class NoScriptView(generic.TemplateView):
    template_name = "registration/no-script.html"
