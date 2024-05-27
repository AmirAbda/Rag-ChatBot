import { useState } from 'react'

import SideBar from './components/SideBar/SideBar'
import Main from './components/Main/Main'
//import ChatComponent from './components/ChatComponent'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <SideBar/>
      <Main/>
    </>
  )
}

export default App
