from rest_framework.response import Response


class CustomResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if isinstance(response.data, dict) and 'status' not in response.data:
            response.data['status'] = 1 if response.status_code == 200 else 0
        return response
