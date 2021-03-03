import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';
import Login from "./components/Login"
import Logout from "./components/Logout"
import EditableTable from "./components/Table"
import AddColumnButton from "./components/AddColumn"
import { useAuth0 } from "@auth0/auth0-react";

// fonts
import "@fontsource/roboto/300.css"
import "@fontsource/roboto/400.css"
import "@fontsource/roboto/500.css"
import "@fontsource/roboto/700.css"

function App() {

const { user, isAuthenticated, isLoading } = useAuth0()

// const initialItems = {'data': [{'initialize':'loading...'}], 'fields':['loading...','initialize']}

const [items, setItems] = useState({'data': [{'initialize':'loading...'}], 'fields':[{'initialize':'loading...'}]})

function GetData() {
  useEffect(() => {
    fetch('/api').then(response => response.json().then(responseData => {
      // console.log(responseData.data)
      setItems(responseData)

    }))
  },[])   
}

  return (
    <div className="App">
        {GetData()}
        <EditableTable  fetch_data={items.data} fetch_fields={items.fields}/>
        <AddColumnButton />
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
