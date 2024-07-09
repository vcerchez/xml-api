from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Doc
from .serializers import DocSerializer


class XMLUploadView(APIView):
    """
    Handle XML file upload.

    This endpoint accepts an XML file upload via a POST request. It processes the
    uploaded file, extracts relevant information, and stores the extracted data in
    the database.

    XML must confirm to the following general schema:

    ```xml
    <STANDARD>
       <META>
           <DOCUMENT.REF>
               <DATE>
           <PUBLICATION.REF>
               ...
               <LG.OJ>
               ...
           <SOURCE>
           <CELEX>
           <TITLE>
       <CONTENU>
           <TITRE>
           <PREAMBULE>
           <ARTICLES>
           <SIGNATURE>
       <ANNEXES>
           ...
    ```

    **Usage:**
    - URL:
    - Method: POST
    - Content-Type: `multipart/form-data`
    - Form Data: A key `file` with the uploaded XML file.

    **Request Example:**
    ```
    POST <URL>
    Content-Type: multipart/form-data

    Form Data:
    - file: <XML file>
    ```

    **Response:**
    - Status 201: File uploaded and processed successfully.
    - Status 400: Bad request, invalid XML file or missing file.

    **Example Response:**
    ```
    {
        "status": "success",
    }
    ```

    **Error Response Example:**
    ```
    {
        "error": "No file provided."
    }
    ```

    **Error Response Example:**
    ```
    {
        "error": "Invalid XML file. "
    }
    ```

    **Notes:**
    - Ensure the uploaded file has the schema expected by the API.
    """

    def post(self, request: Request) -> Response:
        """Handle POST request with uploaded file.

        Args:
            request (Request): Request object

        Returns:
            Response: Response object
        """
        # Get uploaded file
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Parse XML file and save data to database
            Doc.from_xml(file)
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

class DatabaseContentView(mixins.ListModelMixin, 
                    mixins.RetrieveModelMixin, 
                    viewsets.GenericViewSet):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer