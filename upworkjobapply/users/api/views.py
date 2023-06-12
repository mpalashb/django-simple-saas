from rest_framework import (
    generics, response, status, exceptions
)
from users.api.serializers import (
    GenProposalSerializer, CheckScoreSerializer
)

from users.models import (
    Profile, GeneratedProposal, CheckedProposal,
)
from utils.openai_prompt import (
    gen_proposal, check_proposal,
)


class CheckScoreAPIView(generics.GenericAPIView):
    serializer_class = CheckScoreSerializer

    def post(self, request, *args, **kwargs):
        max_len = 2500

        cover_desc = None
        job_desc = None

        serial = self.get_serializer(data=request.data)
        serial.is_valid(raise_exception=True)

        cover_desc = serial.data.get('cover_desc')
        job_desc = serial.data.get('job_desc')

        if len(cover_desc) > max_len or len(job_desc) > max_len:
            raise exceptions.ValidationError(
                {"err": f"Length must be less than {max_len}"})
        try:
            credit_left = self.request.user.profile.credit
        except:
            credit_left = None
        credit_error = '''Make sure you have a profile and enough credit!'''
        status_msg = None

        credit_cost = 10

        if credit_left and credit_left >= credit_cost:

            try:
                profile_ins = Profile.objects.get(user=self.request.user)
            except:
                profile_ins = None

            if profile_ins:
                res = check_proposal(cover_desc=cover_desc, job_desc=job_desc)

                if not res:
                    status_msg = '''No results found!'''

                if res and res.get('result'):

                    profile_ins.credit -= credit_cost
                    profile_ins.save()
                    credit_left = profile_ins.credit

                    CheckedProposal.objects.create(
                        user=request.user.profile,
                        credit_cost=credit_cost
                    )

        else:
            res = {"credit_error": credit_error}
            status_msg = '''You don't have enough credit!'''

        return response.Response({'res': res, 'credit': credit_left, 'status_msg': status_msg}, status=status.HTTP_200_OK)


class GenerateProposalAPIView(generics.GenericAPIView):
    serializer_class = GenProposalSerializer

    def post(self, request, *args, **kwargs):
        max_len = 2500

        serial = self.get_serializer(data=request.data)
        serial.is_valid(raise_exception=True)

        title = serial.data.get('title')
        desc = serial.data.get('desc')
        client_n = serial.data.get('client_n')
        type_pro = serial.data.get('type_pro')

        client_name = client_n
        type_option = type_pro

        if len(title) > max_len or len(desc) > max_len:
            raise exceptions.ValidationError(
                {"err": f"Length must be less than {max_len}"})

        try:
            credit_left = self.request.user.profile.credit
        except:
            credit_left = None

        credit_error = '''Make sure you have a profile and enough credit!'''
        status_msg = None

        credit_cost = 5

        if credit_left and credit_left >= credit_cost:

            try:
                profile_ins = Profile.objects.get(user=self.request.user)
            except:
                profile_ins = None

            if profile_ins:
                res = gen_proposal(
                    title=title,
                    desc=desc,
                    client_name=client_name,
                    type_of=type_option
                )

                GeneratedProposal.objects.create(
                    user=self.request.user.profile,
                    cover_leter=f"{res}"
                )
                if not res:
                    status_msg = '''No results found!'''

                if res:
                    profile_ins.credit -= credit_cost
                    profile_ins.save()
                    credit_left = profile_ins.credit

        else:
            res = credit_error
            status_msg = '''You don't have enough credit!'''

        return response.Response({'res': f'{res}', 'credit': credit_left, 'status_msg': status_msg}, status=status.HTTP_200_OK)
