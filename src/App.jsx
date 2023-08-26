import { useState } from 'react'

import './App.css'
import PromptForm from './components/PromptForm'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>Slidey</h1>
      </header>

      <PromptForm />
    </div>
  )
}

export default App
