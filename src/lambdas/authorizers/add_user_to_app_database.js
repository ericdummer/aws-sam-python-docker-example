/**
* Handler that will be called during the execution of a PostUserRegistration flow.
*
* @param {Event} event - Details about the context and user that has registered.
* @param {PostUserRegistrationAPI} api - Methods and utilities to help change the behavior after a signup.
*/

const axios = require("axios");
const created_at = new Date(Date.now()).toISOString();

/**
 * @param {Event} event - Details about registration event.
 */
exports.onExecutePostUserRegistration = async (event) => {
  const user_id = event.user.user_id
  const email = event.user.email 
  
  const url = 'https://ethos.hasura.app/v1/graphql';
  const query = `mutation InsertNewUser($user_id: String!, $email: String!, $created_at: timestamptz!) {
    insert_app_users_one(object: {created_at: $created_at, email: $email, id: $user_id, updated_at: $created_at, updated_by: $user_id}) {
      id
    }
  }`
  const variables = { user_id, email, created_at}
  const config = { headers: {'content-type' : 'application/json', 'x-hasura-admin-secret': event.secrets.hasura_admin_secret},
    }

  await axios.post(url, {
        query: query,
        variables: variables
      }, config)
    .then(res => {
      console.log(res.data)
    })
    .catch(err => {
      console.log("POST error: ", err)
    })
    
};


