FROM public.ecr.aws/lambda/python:3.11
## KEEP THIS AT 3.11 - PANDAS IS NOT COMPATIBLE WITH 3.12
COPY lambdas/consumers/consumer_1/requirements.txt ./
RUN python3.11 -m pip install -r requirements.txt -t .
COPY services ./services  
COPY models ./models  
COPY utilities ./utilities  
COPY lambdas/consumers/consumer_1/test_documents ./test_documents
COPY lambdas/consumers/consumer_1/consumer_1_lambda.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["consumer_1.lambda_handler"]