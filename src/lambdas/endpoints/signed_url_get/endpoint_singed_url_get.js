/*
  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

'use strict'

const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.AWS_REGION })
const s3 = new AWS.S3()

// Change this value to adjust the signed URL's expiration
const URL_EXPIRATION_SECONDS = 300

const cors_headers = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'OPTIONS,HEAD,GET,POST',
  'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
}

// Main Lambda entry point
exports.handler = async (event) => {
  const httpMethod = event.requestContext.http.method;

  if (httpMethod === 'OPTIONS' || httpMethod === 'HEAD') {
    return {
      statusCode: 200,
      headers: cors_headers
    }
  }

  return await getUploadURL(event)
}

const getUploadURL = async function(event) {

  var file_path = ''
  var content_type = ''
  if (event.queryStringParameters && event.queryStringParameters.file_path) {
    file_path = event.queryStringParameters.file_path
    console.log('file_path: ', file_path) 
  }
  if (event.queryStringParameters && event.queryStringParameters.content_type) {
    content_type = event.queryStringParameters.content_type
    console.log('content_type: ', content_type)
  }

  if (file_path == '' || content_type == '') {
    return JSON.stringify({
      statusCode: 400,
      body: JSON.stringify({ error: 'file_path and content_type is required'})
    })
  }

  const allowedContentTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif'];
  const contentTypeLowerCase = content_type.toLowerCase().trim(); 

  if (!allowedContentTypes.includes(contentTypeLowerCase)) {
    return JSON.stringify({
      statusCode: 400,
      body: JSON.stringify({ error: 'Invalid content type: ' + content_type})
    })
  }

  // Get signed URL from S3
  const s3Params = {
    Bucket: process.env.S3_UPLOAD_BUCKET,
    Key: file_path,
    Expires: URL_EXPIRATION_SECONDS,
    ContentType: content_type,

    // This ACL makes the uploaded object publicly readable. You must also uncomment
    // the extra permission for the Lambda function in the SAM template.
    // ACL: 'public-read'
  }
  // console.log('s3Params: ', s3Params)

  try{
    const upload_url = await s3.getSignedUrlPromise('putObject', s3Params)

    return {
      headers: cors_headers,
      statusCode: 200,
      body: JSON.stringify({  
        status_code: 200,
        upload_url: upload_url,
        file_path: file_path,
        content_type: content_type
      })
    }

  } catch (err) {
    console.error(err)
    return JSON.stringify({
      statusCode: 500,
      body: JSON.stringify({ error: 'failed to create signed url'})
    })
  }
}