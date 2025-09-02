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
  // userPoolId: process.env.REACT_APP_CAVENDISH_AWS_POOL_ID,
  // userPoolClientId: process.env.REACT_APP_CAVENDISH_AWS_CLIENT_ID,
  // cognitoDomain: process.env.REACT_APP_CAVENDISH_AWS_COGNITO_DOMAIN,
  // stage: process.env.REACT_APP_STAGE,
  // rumApplicationId: process.env.REACT_APP_RUM_APPLICATION_ID,
  // rumClientToken: process.env.REACT_APP_RUM_CLIENT_TOKEN,
  // rumSite: 'datadoghq.eu'
};
