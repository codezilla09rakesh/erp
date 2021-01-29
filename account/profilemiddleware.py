from account.models import MyProfile
from account.models import CustomUser

class GetProfile:
    def __init__(self, get_response):
        self.get_response = get_response
    #
    # def process_template_response(self, request, response):
    #     if request.user.is_authenticated:
    #         user = CustomUser.objects.get(username = request.user)
    #         try:
    #             get_profile = MyProfile.objects.get(user = user)
    #         except:
    #             get_profile = None
    #         print('I am in side on proces', get_profile)
    #         response.context_data['get_profile'] = get_profile
    #     # if not ('notification_count' in response.context_data):
    #     #     response.context_data['notification_count'] = 2
    #     return response

    def __call__(self, request):
        # print('in side on middleware')
        if request.user.is_authenticated:
            user = CustomUser.objects.get(username = request.user)
            # print('user find')
            try:
                get_profile = MyProfile.objects.get(user = user)
                # get_profile = True
            except:
                get_profile = False
            request.get_profile = get_profile
        response = self.get_response(request)
        return response