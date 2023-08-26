import { useEffect, useState } from 'react';
import { Button, Grid, TextField } from '@mui/material';

const GOOGLE_SLIDES_URL_REGEX =
    /https:\/\/docs\.google\.com\/presentation\/d\/([a-zA-Z0-9_-]+)/;

export default function PromptForm() {
  const [prompt, setPrompt] = useState("");
  const [mood, setMood] = useState("");

  function clearForm() {
    setPrompt("");
    setMood("");
  }

  function submitPrompt(event) {
    event.preventDefault();

    chrome.tabs.query({active: true, currentWindow: true})
        .then(([tab]) => {
          if (GOOGLE_SLIDES_URL_REGEX.test(tab.url)) {
            console.log("matched");
            return chrome.scripting.executeScript({
              target: {tabId: tab.id},
              func: () => {
                const SELECTED_ELEMENT_COLOUR = "#8ab4f8";
                const selectedElementDOMElement =
                    document.querySelector(`path[stroke="${SELECTED_ELEMENT_COLOUR}"]`);

                // If no element is selected, return null
                if (selectedElementDOMElement === null) {
                  return null;
                }

                // Parent is 3 nodes above
                let targetElement = selectedElementDOMElement;
                while (!targetElement.hasAttribute("id")) {
                  targetElement = targetElement.parentElement;
                }

                // Now, get the object ID from the `id` attribute
                const objectID = targetElement.id;
                return objectID;
              },
            });
          } else {
            return null;
          }
        }).then((results) => {
          const selectedObjectID = results !== null ? results[0].result : null;
          const jsonData = {
            prompt,
            mood,
            objectID: selectedObjectID,
          };
          
          return jsonData;
        }).then((jsonData) => {
          return fetch("http://localhost:5000/prompt-processing", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(jsonData),
          });
        }).then((data) => {
          return data.json();
        }).then((jsonResponseData) => {
          if (jsonResponseData.status != "OK") {
            throw new Error("bad status");
          }
        }).then(() => {
          clearForm();
        }).catch((error) => {
          console.error(error);
        });
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
          size="small"
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
          size="small"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
        />
      </Grid>

      <Grid item xs={12}>
        <Button type="submit" variant="contained">Send Prompt</Button>
      </Grid>
    </Grid>
  );
}
