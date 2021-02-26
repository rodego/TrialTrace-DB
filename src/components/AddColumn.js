import React, {useEffect} from "react";
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';


const LoginButton = () => {

    useEffect(() => {
      fetch('/api').then(response => response.json().then(responseData => {
        // console.log(responseData.data)
        setItems(responseData)

      }))
    }, [])   

  return <Button 
                variant="contained" 
                color="primary" 
                disableElevation 
                onClick={
                    () => loginWithRedirect()
                    }
                >
                Log In
            </Button>;
};

export default LoginButton;