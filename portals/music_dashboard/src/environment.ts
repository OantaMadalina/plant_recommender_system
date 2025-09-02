const environment = {
  apiUrl: process.env.REACT_APP_API_URL,
  params: {
    headers: {
      "x-api-key": process.env.REACT_APP_API_KEY,
    },
    crossdomain: true,
  },
};

export default environment;
