class ResponseStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Custom middleware is being executed.")  # Add this line

        response = self.get_response(request)

        # Check if the response is an error response
        if response.status_code >= 400:
            status = 0  # Error
        else:
            status = 1  # Success
        # Add the status field to the response
        response['status'] = status
        print(response['status'])

        return response
