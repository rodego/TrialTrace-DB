import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return <Button variant="contained" color="primary" disableElevation onClick={() => loginWithRedirect()}>Log In</Button>;
};

export default LoginButton;