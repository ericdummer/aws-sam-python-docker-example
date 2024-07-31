/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/

const axios = require("axios");


exports.onExecutePostLogin = async (event, api) => {
   const user_id = event.user.user_id;
  const email = event.user.email ;
  const updated_at = new Date(Date.now()).toISOString();
  const email_verified = event.user.email_verified;
  const last_pw_update = event.user.last_password_reset
  
  const url = 'https://ethos.hasura.app/v1/graphql';
  const query = `mutation UpdateUser($user_id: String!, $email: String!, $updated_at: timestamptz!, $last_pw_update: timestamptz!, $email_verified: Boolean!) {
  update_app_users_by_pk(pk_columns: {id: $user_id}, _set: {email: $email, updated_at: $updated_at, updated_by: $user_id, last_pw_updated: $last_pw_update, email_verified: $email_verified}) {
      id
    }
  }`
  const variables = { user_id, email, updated_at, last_pw_update, email_verified}
  const config = { headers: {'content-type' : 'application/json', 'x-hasura-admin-secret': event.secrets.hasura_admin_secret},
    }

  await axios.post(url, {
        query: query,
        variables: variables
      }, config)
    .then(res => {
      console.log(res.data)
      // TODO: If failure is because { data: { update_trulease_users_by_pk: null } } then try an insert?
    })
    .catch(err => {
      console.log("POST error: ", err)
    })
};