import Vue from 'vue'
import Amplify from '@aws-amplify/core'

Amplify.configure({
  aws_project_region: process.env.REGION,
  aws_cognito_region: process.env.REGION,
  aws_user_pools_id: process.env.COGNITO_USERPOOL_ID,
  aws_user_pools_web_client_id: process.env.COGNITO_USERPOOL_CLIENT_ID,
  oauth: {},
  Auth: {
    region: process.env.REGION,
    userPoolId: process.env.COGNITO_USERPOOL_ID,
    userPoolWebClientId: process.env.COGNITO_USERPOOL_CLIENT_ID,
  },
})

Vue.prototype.$Amplify = Amplify
