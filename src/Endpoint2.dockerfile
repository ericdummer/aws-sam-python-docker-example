FROM public.ecr.aws/lambda/python:3.12
COPY lambdas/endpoints/endpoint_2/requirements.txt ./
RUN python3.12 -m pip install -r requirements.txt -t .
COPY services/db_service.py ./services/db_service.py  
COPY services/secrets_service.py ./services/secrets_service.py  
COPY lambdas/endpoints/document_get/endpoint_2_lambda.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["endpoint_2_lambda.lambda_handler"]


