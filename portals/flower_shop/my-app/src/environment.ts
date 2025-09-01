export default {
    apiPath: process.env.REACT_APP_CAVENDISH_PORTAL_API_URI,
    params: {
      headers: {
        'x-api-key': process.env.REACT_APP_CAVENDISH_PORTAL_API_KEY,
        // 'x-apigw-api-id': process.env.REACT_APP_CAVENDISH_PORTAL_API_HOST
      },
      crossdomain: true
    },
    awsRegion: process.env.REACT_APP_CAVENDISH_AWS_REGION,
  };