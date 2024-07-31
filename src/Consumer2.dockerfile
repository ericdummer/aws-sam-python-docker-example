FROM public.ecr.aws/lambda/python:3.12
COPY lambdas/consumers/consumer_2/requirements.txt ./
RUN python3.12 -m pip install -r requirements.txt -t .
COPY utilities ./utilities  
COPY models ./models  
COPY services ./services  
COPY lambdas/consumers/consumer_2/consumer_2_lambda.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["consumer_2.lambda_handler"]