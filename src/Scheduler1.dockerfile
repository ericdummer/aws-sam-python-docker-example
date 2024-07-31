FROM public.ecr.aws/lambda/python:3.12
COPY lambdas/schedulers/scheduler_1/requirements.txt/ ./
RUN python3.12 -m pip install -r requirements.txt -t .
COPY services ./services
COPY lambdas/schedulers/scheduler_1/scheduler_1_lambda.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["scheduler_1_lambda.lambda_handler"]