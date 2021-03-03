import React, {useEffect} from "react";
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';


const AddColumnButton = () => {

  const data = { 
                field_name:  'Column', 
                field_note:  'test',
                field_meta:  'user generated',
                };

  const addColumn = data => fetch('/api/newcol', {
                                                  method: 'POST', // or 'PUT'
                                                  headers: {
                                                    'Content-Type': 'application/json',
                                                  },
                                                  body: JSON.stringify(data),
                                                })
                                                .then(response => response.json())
                                                .then(data => {
                                                  console.log('Success:', data);
                                                })
                                                .catch((error) => {
                                                  console.error('Error:', error);
                                                });

  return <Button 
                variant="contained" 
                color="primary" 
                disableElevation 
                onClick={
                    () => addColumn(data)
                    }
                >
                Add Column
            </Button>;
};

export default AddColumnButton;