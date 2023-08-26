import { useState } from 'react'
import { Button, Grid, TextField } from '@mui/material';

export default function PromptForm() {
  const [prompt, setPrompt] = useState("")
  const [mood, setMood] = useState("")

  function clearForm() {
    setPrompt("")
    setMood("")
  }

  function submitPrompt(event) {
    event.preventDefault()
  
    const jsonData = {prompt, mood}
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
  
    clearForm()
  }

  return (
    <Grid
      component="form"
      container
      spacing={2}
      onSubmit={submitPrompt}
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
        <TextField
          id="mood-input"
          label="Mood"
          helperText="Enter a mood to jazz up your presentation!"
          fullWidth
          value={mood}
          onChange={(e) => setMood(e.target.value)}
        />
      </Grid>

      <Grid item xs={12}>
        <Button type="submit" variant="contained">Send Prompt</Button>
      </Grid>
    </Grid>
  )
}
