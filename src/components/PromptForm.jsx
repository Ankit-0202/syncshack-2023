import { useState } from 'react'
import { Button, Grid, TextField } from '@mui/material';

function submitPrompt(event, prompt, setPromptCallback) {
  event.preventDefault()

  const jsonData = {prompt}
  fetch("http://localhost:5000/prompt-processing", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonData),
  }).then((data) => {
    return data.json()
  }).then((jsonResponseData) => {
    if (jsonResponseData.status != "OK") {
      throw new Error("bad status")
    }
  }).catch((error) => {
    console.error(error)
  })

  setPromptCallback("")
}

export default function PromptForm() {
  const [prompt, setPrompt] = useState("")

  return (
    <Grid
      component="form"
      container
      spacing={2}
      onSubmit={(e) => submitPrompt(e, prompt, setPrompt)}
    >
        <Grid item xs={12}>
          <TextField
            id="prompt-input"
            label="Prompt input"
            multiline
            fullWidth
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}>
          <Button type="submit" variant="contained">Send Prompt</Button>
        </Grid>
    </Grid>
  )
}
