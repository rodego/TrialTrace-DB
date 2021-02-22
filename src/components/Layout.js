import React, {useMemo, useEffect, useState} from "react"
import { useTable, useSortBy } from 'react-table'
 
 function Layout(props) {

   const initialItems = {'data': [{'we':'are wilds'}]}

   const [items, setItems] = useState({'data': []})

    useEffect(() => {
      fetch('/api').then(response => response.json().then(responseData => {
        // console.log(responseData.data)
        setItems(responseData)

      }))
    }, [])   



   const data = useMemo(() => [...items.data], [items.data])
 

    // console.log('data')
    console.log('columns')
    console.log(get_keys(items.data))

    function get_keys(props) {

      const unique = [...new Set (props.flatMap(i => Object.keys(i)))]
     
      return ( unique.map((key, index) => ({Header : `Column${index + 1}`, accessor : `${key}`})))

    }


 
   const columns = useMemo(

     () => [...get_keys(items.data)],
     
     
    //  () =>
    //  [
    //    {
    //      Header: 'Column 1',
    //      accessor: 'col1', // accessor is the "key" in the data
    //    },
    //    {
    //      Header: 'Column 2',
    //      accessor: 'col2',

    //    },
    //  ],
     [items.data]
   )

  
 
   const {
     getTableProps,
     getTableBodyProps,
     headerGroups,
     rows,
     prepareRow,
   } = useTable({ columns, data },
    useSortBy)
 
   return (
     <table {...getTableProps()} style={{ border: 'solid 1px blue' }}>
       <thead>
         {headerGroups.map(headerGroup => (
           <tr {...headerGroup.getHeaderGroupProps()}>
             {headerGroup.headers.map(column => (
               <th
                 {...column.getHeaderProps(column.getSortByToggleProps())}
                 style={{
                   borderBottom: 'solid 3px red',
                   background: 'aliceblue',
                   color: 'black',
                   fontWeight: 'bold',
                 }}
               >
                 {column.render('Header')}
               </th>
             ))}
           </tr>
         ))}
       </thead>
       <tbody {...getTableBodyProps()}>
         {rows.map(row => {
           prepareRow(row)
           return (
             <tr {...row.getRowProps()}>
               {row.cells.map(cell => {
                 return (
                   <td
                     {...cell.getCellProps()}
                     style={{
                       padding: '10px',
                       border: 'solid 1px gray',
                       background: 'papayawhip',
                     }}
                   >
                     {cell.render('Cell')}
                   </td>
                 )
               })}
             </tr>
           )
         })}
       </tbody>
     </table>
   )
 }


 export default Layout

