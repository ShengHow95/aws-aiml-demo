const awsmobile = {
  aws_project_region: process.env.REGION,
  aws_cognito_region: process.env.REGION,
  aws_user_pools_id: process.env.COGNITO_USERPOOL_ID,
  aws_user_pools_web_client_id: process.env.COGNITO_USERPOOL_CLIENT_ID,
}

export default awsmobile
