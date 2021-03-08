import React, {useMemo, useEffect, useState} from "react"
import {useTable, useSortBy, useColumnOrder, useResizeColumns, useBlockLayout} from 'react-table'

//material-ui
import {TextField} from '@material-ui/core'
import IconButton from '@material-ui/core/IconButton';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Popover from '@material-ui/core/Popover';
import FormGroup from '@material-ui/core/FormGroup';
import { ArrowDownward, ArrowUpward, MoreVert} from '@material-ui/icons';

//custom components
import AddColumn from './AddColumn'

//style
import tableStyle from './Table.module.css'



//Functions
const globalIconSize = 'small'

function shuffle(arr) {
  arr = [...arr]
  const shuffled = []
  while (arr.length) {
    const rand = Math.floor(Math.random() * arr.length)
    shuffled.push(arr.splice(rand, 1)[0])
  }
  return shuffled
}




// Create an editable cell renderer
const EditableCell = ({
    value: initialValue,
    row: {original},
    column: {id},
    updateMyData, // This is a custom function that we supplied to our table instance
}) => { // We need to keep and update the state of the cell normally
    const [value, setValue] = useState(initialValue)
    const [show, setShow] = useState(false)
    // const [history, setHistory] = useState(false)

    const handleClick = e => {
        // if(e.ctrlKey) {
        setShow(!show)
        // getCellHistory(index,id)
        // console.log(e) 
        // }
    }

    const handleKeyPress = e => {
        if(e.metaKey && (e.keyCode === 13 || e.keyCode === 83)  ) {
        e.preventDefault()
        setShow(!show)
        handleBlur()
        // console.log(e) 
        }
        if(e.keyCode === 27) {
        setShow(!show)
        handleBlur()
        }
    }


    const handleChange = e => {
        if(show) {
        setValue(e.target.value)
        }
    }

    // We'll only update the external data when the input is blurred
    const handleBlur = () => {
        updateMyData(id, value)
        console.log(id, original.rowid, value)
    }

    // If the initialValue is changed external, sync it up with our state
    useEffect(() => {
        setValue(initialValue)
    }, [initialValue])

    return (
        <>
    <div onDoubleClick={handleClick}
    style = {{
        height: '60px',
        }}
        id = 'popover-anchor'
    >
    <div
    style = {{
        display: show ? 'none': 'block',
    }}
    >{value}</div>

    <Popover 
    // style ={{
    //     display: show ? 'block': 'none',
    //     // backgroundColor: 'papayawhip'
    //     // position: 'absolute',
    //     }}
        open = {show}
        anchorEl = '#popover-anchor'
        anchorOrigin={{
            vertical: 'center',
            horizontal: 'center',
        }}
        transformOrigin={{
            vertical: 'center',
            horizontal: 'center',
        }}
        >
    <FormGroup>
        <TextField id="standard-basic" label="datapoint" 
            value={value}
            onChange={handleChange}
            onBlur={handleBlur}
            onKeyDown={handleKeyPress}   
            multiline     
        />
        <TextField id="standard-basic" label="note" 
            // value={value}
            // onChange={handleChange}
            onBlur={handleBlur}
            onKeyDown={handleKeyPress}   
            multiline

        />
    </FormGroup>
    </Popover>
    </div>
    </>
                  )
}

// Set our editable cell renderer as the default Cell renderer
const defaultColumn = {
    Cell: EditableCell,
    minWidth: 30,
    width: 400,
    // maxWidth: 400,
}




function BasicTable ({columns, data, updateMyData, skipPageReset}) {


const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    visibleColumns,
    setColumnOrder,
} = useTable({
    columns,
    data,
    defaultColumn,
    // use the skipPageReset option to disable page resetting temporarily
    autoResetPage: !skipPageReset,
    // updateMyData isn't part of the API, but
    // anything we put into these options will
    // automatically be available on the instance.
    // That way we can call this function from our
    // cell renderer!
    updateMyData
}, 
    useSortBy,    
    useColumnOrder,
    useBlockLayout,
    useResizeColumns
)

const randomizeColumns = () => {
    setColumnOrder(shuffle(visibleColumns.map(d => d.id)))
}





return (
    <TableContainer component={Paper}>
    {/* <button onClick={() => randomizeColumns({})}>Randomize Columns</button> */}
    <Table stickyHeader={true} {...getTableProps()}>
        <TableHead >{
            headerGroups.map(headerGroup => (
                <TableRow 
                {...headerGroup.getHeaderGroupProps()}
                >{headerGroup.headers.map(column => (

                        <TableCell 
                        // {...column.getHeaderProps(column.getSortByToggleProps())}
                        {...column.getHeaderProps()}
                        >

                        <span style={{verticalAlign: 'middle'}}>{
                            column.render('Header')
                        }</span>
                        <span style={{verticalAlign: 'middle'}}
                        className={tableStyle.headerButton}
                        ><IconButton size={globalIconSize}
                        {...column.getSortByToggleProps()}
                        >
                        {
                                column.isSorted ? column.isSortedDesc ? <ArrowDownward fontSize={globalIconSize}/> : <ArrowUpward fontSize={globalIconSize}/> : <MoreVert fontSize={globalIconSize}/>
                            }
                        </IconButton></span>
                        <span style={{verticalAlign: 'middle'}}
                            {...column.getResizerProps()}
                            className={`${tableStyle.resizer} ${
                                column.isResizing ? tableStyle.isResizing : ''
                            }`}
                         >
                         <svg className={tableStyle.columnSeparator} focusable="false" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M11 19V5h2v14z"></path>
                         </svg>
                         
                         </span>
                        </TableCell>

                    ))
                }</TableRow>))
        }</TableHead>
        <TableBody {...getTableBodyProps()}>
            {
            rows.map(row => {
                prepareRow(row)
                return (
                    <TableRow {...row.getRowProps()}
                    >{row.cells.map(cell => {
                            return (
                                <TableCell {...cell.getCellProps()} >
                                <div
                                style={{height: 100,
                                        // minWidth: 30,
                                        overflow: 'scroll'}}
                                >
                                <p>
                                {cell.render('Cell')}
                                </p>
                                </div>
                                </TableCell>
                            )
                        })
                    }</TableRow>
                )
            })
        }</TableBody>
    </Table>
    </TableContainer>
)}


function EditableTable ({fetch_data, fetch_fields}) {





function map_fields(props) {

    const cols = props.map(x => ({Header: `${
            Object.values(x)
        }`, accessor: `${
            Object.keys(x)
        }`}))

    return(cols)
}


const columns = useMemo(() => [...map_fields(fetch_fields)], [fetch_fields, fetch_data])

const dataset = useMemo(() => [...fetch_data], [fetch_fields,fetch_data])


const [data, setData] = useState(dataset)
// const [originalData] = useState(data)
const [skipPageReset, setSkipPageReset] = useState(false)
// console.log(data)
// console.log(dataset)
// setData(dataset)

//force an update to get past loading screen
useEffect(() => {setData(dataset)},[fetch_fields,fetch_data])

// We need to keep the table from resetting the pageIndex when we
// Update data. So we can keep track of that flag with a ref.

// When our cell renderer calls updateMyData, we'll use
// the rowIndex, columnId and new value to update the
// original data
const updateMyData = (rowIndex, columnId, value) => { // We also turn on the flag to not reset the page
    setSkipPageReset(true)
    setData(old => old.map((row, index) => {
        if (index === rowIndex) {
            return {
                ...old[rowIndex],
                [columnId]: value
            }
        }
        return row
    }))
}

// After data chagnes, we turn the flag back off
// so that if data actually changes when we're not
// editing it, the page is reset
useEffect(() => {
    setSkipPageReset(false)
}, [data])

// Let's add a data resetter/randomizer to help
// illustrate that flow...
// const resetData = () => setData(originalData)

return (
    <>
        <BasicTable 
            columns={columns}
            data={data}
            updateMyData={updateMyData}
            skipPageReset={skipPageReset}/>
    </>
)}

export default EditableTable
