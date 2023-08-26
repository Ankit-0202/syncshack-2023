import { useState } from 'react'
import { Box, Button, Grid, TextField } from '@mui/material';

export default function PromptForm() {
  const [prompt, setPrompt] = useState("")

  return (
    <Grid component="form" container spacing={2}>
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
