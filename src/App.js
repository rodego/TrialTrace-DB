import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';
import Login from "./components/Login"
import Logout from "./components/Logout"
import EditableTable from "./components/Table"
import AddColumnButton from "./components/AddColumn"
import IconButton from '@material-ui/core/IconButton';  
import { useAuth0 } from "@auth0/auth0-react";
import {Refresh} from '@material-ui/icons';

// fonts
import "@fontsource/roboto/300.css"
import "@fontsource/roboto/400.css"
import "@fontsource/roboto/500.css"
import "@fontsource/roboto/700.css"

function App() {

const { user, isAuthenticated, isLoading } = useAuth0()

const initialItems = {'data': [{'initialize':'loading...'}], 'fields':[{'initialize':'loading...'}]}

const [items, setItems] = useState(initialItems)

const GetData = () => {
    fetch('/api').then(response => response.json().then(responseData => {
      // console.log(responseData.data)
      setItems(responseData)
      console.log('refreshed')

    }))
  }

  useEffect(() => {
        GetData()
    }, [])

  return (
    <div className="App">
        <IconButton onClick={GetData}> 
        <Refresh/>
        </IconButton>
        <AddColumnButton triggerRefresh={GetData}/>
        <EditableTable  fetch_data={items.data} fetch_fields={items.fields}/>
        {/* {isAuthenticated ? 
        <>
        <Logout /> 
        <Layout />
        </>
        : <Login />} */}
    </div>
  );
}

export default App;
